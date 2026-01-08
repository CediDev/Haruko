from functools import partial
from itertools import chain
from typing import cast
from enum import Enum

import discord
from discord import Member, TextChannel, User, app_commands, Thread
from discord.ext.commands import Bot, Cog, command
from discord.enums import InteractionType, ComponentType

from sqlmodel import Field, SQLModel, select, Session, create_engine, update


from constants import (
    ADMIN_PRIVILEDGE_ROLES,
    CEDISZ_ID,
    FULL_EMOJI,
    POLLS_PRIVILEDGE_ROLES,
    ST_ADMIN_SERVER_ID,
    PollType,
    PrivacyButtonText,
    RoleId,
)


UserId = int


class PollData(SQLModel):
    author_id: UserId
    title:str
    options: list[str | None]
    option_votes_map: dict[int, list[UserId]]
    multiple_choice: bool
    show_results: bool
    privacy_button_label: str
    privacy_button_style: int
    
class PollDB(SQLModel, table=True):
    __tablename__ = "Poll"  # type: ignore
    poll_id: int | None = Field(default=None, primary_key=True)
    message_id: int
    poll_data: str


def _check_priviledge(member: discord.Member, priviledged_roles: list[RoleId]) -> bool:
    return bool(set(role.id for role in member.roles) & set(role.value for role in priviledged_roles))


BUTTON_ID = "{poll_id}:{button_type}:{button_index}"


class ButtonType(Enum):
    OPTION_VOTE = "OPTION_VOTE"
    NON_VOTERS = "NON_VOTERS"
    RESULTS = "RESULTS"
    PRIVACY = "PRIVACY"


class Poll(discord.ui.View):
    def __init__(
        self,
        poll_id: int,
        title: str,
        author: Member,
        multiple_choice: bool,
        options: list[str | None],
        options_votes_map: dict[int, list[User | Member]] | None = None,
        show_results: bool = False,
        privacy_button_label:str = PrivacyButtonText.PRIVATE.value,
        privacy_button_style: discord.ButtonStyle = discord.ButtonStyle.red,
        
        ) -> None:
        self.poll_id: int = poll_id
        self.multiple_choice: bool = multiple_choice
        self.option_votes_map = options_votes_map if options_votes_map else {index:[] for index in range(len(options))}
        self.author = author
        self.show_results: bool = show_results
        self.options = options
        self.title: str = title
        self.privacy_button: discord.ui.Button | None = None
        
        super().__init__(timeout=None)
        self.add_buttons(privacy_button_label=privacy_button_label, privacy_button_style=privacy_button_style)

    def dump_data(self) -> PollData:
        return PollData(
            author_id=self.author.id,
            title=self.title,
            options=self.options,
            option_votes_map={option_index: [voter.id for voter in votes] for option_index, votes in self.option_votes_map.items()},
            show_results=self.show_results,
            multiple_choice=self.multiple_choice,
            privacy_button_label=self.privacy_button.label, #type:ignore
            privacy_button_style=self.privacy_button.style.value #type:ignore
        )

    @property
    def unique_voters(self) -> list[User | Member]:
        return list(set(chain.from_iterable(
            _voters for _voters in self.option_votes_map.values()
        )))

    @property
    def total_votes(self) -> int:
        return len(list(chain.from_iterable(_voters for _voters in self.option_votes_map.values())))

    @property
    def unique_votes(self) -> int:
        return len(self.unique_voters)
    
    async def get_user_votes(self, user: User) -> list[int]:
        return [option_index for option_index, votes in self.option_votes_map.items() if user in votes]
    
    async def make_embed(self) -> discord.Embed:
        DESCRIPTION = "Liczba głosów: {total_votes} | Liczba głosujących: {unique_votes}"
        embed = discord.Embed(
            title=f"{self.title} | {self.privacy_button.label}", #type:ignore
            description=DESCRIPTION.format(total_votes=self.total_votes, unique_votes=self.unique_votes),
            color=discord.Colour.pink(),
        )
        
        match self.show_results, PrivacyButtonText(self.privacy_button.label): # type: ignore
            case True, PrivacyButtonText.PRIVATE:
                for option, votes in zip(self.options, self.option_votes_map.values(), strict=True):
                    if option:
                        embed.add_field(name=f"{FULL_EMOJI} {option}", value="> " + str(len(votes)) + " głosów")
            case True, PrivacyButtonText.PUBLIC:
                for option, votes in zip(self.options, self.option_votes_map.values(), strict=True):
                    if option:
                        embed.add_field(
                            name=f"{FULL_EMOJI} {option}",
                            value="> " + str(len(votes)) + f" głosów\n{', '.join(user.name for user in votes)}",
                        )
        return embed
    
    def add_buttons(self, privacy_button_label: str, privacy_button_style: discord.ButtonStyle):
        privacy_button = discord.ui.Button(
            label=privacy_button_label,
            style=privacy_button_style,
            row=2,
            custom_id=BUTTON_ID.format(
                poll_id=self.poll_id,
                button_type=ButtonType.PRIVACY.value,
                button_index=0,
            ),
        )
        privacy_button.callback = self._set_privacy
        self.privacy_button = privacy_button

        results_button = discord.ui.Button(
            label="Podaj wyniki",
            style=discord.ButtonStyle.blurple,
            row=2,
            custom_id=BUTTON_ID.format(
                poll_id=self.poll_id,
                button_type=ButtonType.RESULTS.value,
                button_index=0,
            ),
        )
        results_button.callback = self._get_results
        
        nonvoters_visibility_button = discord.ui.Button(
            label="Niegłosujący",
            row=2,
            custom_id=BUTTON_ID.format(
                poll_id=self.poll_id,
                button_type=ButtonType.NON_VOTERS.value,
                button_index=0,
            ),
        )
        nonvoters_visibility_button.callback = self._show_nonvoters
        
        for option_index, option in enumerate(self.options):
            if option:
                button = discord.ui.Button(
                    label=option,
                    style=discord.ButtonStyle.secondary,
                    row=1,
                    custom_id=BUTTON_ID.format(
                        poll_id=self.poll_id,
                        button_type=ButtonType.OPTION_VOTE.value,
                        button_index=option_index,
                    ),
                )
                button.callback = partial(self._option_button, index = option_index)
                self.add_item(button)
        
        self.add_item(nonvoters_visibility_button)
        self.add_item(results_button)
        self.add_item(privacy_button)

    async def _option_button(self, interaction:discord.Interaction, index: int):
            votes = await self.get_user_votes(cast(User, interaction.user))
            if index in votes:
                await interaction.response.send_message("Już zagłosowałeś na tę opcję!", ephemeral=True)
                return
            if self.multiple_choice:
                self.option_votes_map[index].append(interaction.user)
                await interaction.response.edit_message(embeds=[await self.make_embed()], view=self)
                await interaction.followup.send("Pomyślnie oddano głos!", ephemeral=True)
                return
            else:
                self.option_votes_map[index].append(interaction.user)
                if votes:  # non-empty list -> user already voted
                    option_index = votes[0]  # single choice poll means that there is only one vote in votes
                    self.option_votes_map[option_index].remove(interaction.user)
                    await interaction.response.edit_message(embeds=[await self.make_embed()], view=self)
                    await interaction.followup.send("Pomyślnie zmieniono głos!", ephemeral=True)
                else:
                    await interaction.response.edit_message(embeds=[await self.make_embed()], view=self)
                    await interaction.followup.send("Pomyślnie oddano głos!", ephemeral=True)

    async def _set_privacy(self, interaction:discord.Interaction):
                assert isinstance(interaction.user, Member)
                assert self.privacy_button
                if interaction.user.id == CEDISZ_ID or _check_priviledge(interaction.user, ADMIN_PRIVILEDGE_ROLES):
                    self.privacy_button.style = discord.ButtonStyle.blurple if self.privacy_button.style == discord.ButtonStyle.red else discord.ButtonStyle.red
                    self.privacy_button.label = PrivacyButtonText.PUBLIC.value if self.privacy_button.label == PrivacyButtonText.PRIVATE.value else PrivacyButtonText.PRIVATE.value
                    await interaction.response.edit_message(embeds=[await self.make_embed()], view=self)
                else:
                    await interaction.response.send_message("Nie masz permisji!", ephemeral=True)

    async def _get_results(self, interaction:discord.Interaction):
                print("results1")
                assert isinstance(interaction.user, Member)
                print("results2")
                if interaction.user.id == CEDISZ_ID or interaction.user.id == self.author.id or _check_priviledge(interaction.user, ADMIN_PRIVILEDGE_ROLES):
                    print("results3")
                    self.show_results = not self.show_results  # inverts results visibility setting
                    await interaction.response.edit_message(embeds=[await self.make_embed()], view=self)
                else:
                    print("results4")
                    await interaction.response.send_message("Nie masz permisji!", ephemeral=True)

    async def _show_nonvoters(self, interaction:discord.Interaction):
            if interaction.user.id == CEDISZ_ID or interaction.guild_id == ST_ADMIN_SERVER_ID or _check_priviledge(cast(Member, interaction.user), ADMIN_PRIVILEDGE_ROLES):
                if isinstance(interaction.channel, discord.TextChannel):
                    #discord.Thread: belongs to TextChannel or ForumChannel
                    able_to_vote = interaction.channel.members
                elif isinstance(interaction.channel, discord.Thread):
                    able_to_vote = [interaction.guild.get_member(member.id) for member in await interaction.channel.fetch_members()]
                else: 
                    raise AssertionError("channel is neither TextChannel nor Thread")
                nonvoters = [member for member in able_to_vote if member not in self.unique_voters and not member.bot]
                message_str = "Brak oddanego głosu: "
                for member in nonvoters:
                    message_str += f"{member.name}, "
                await interaction.response.send_message(message_str, ephemeral=True)
            else:
                await interaction.response.send_message("Nie masz permisji!", ephemeral=True)


class Polls(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.polls: dict[int, Poll] = {}
        self.current_session_polls: dict[int, Poll] = {}
        
        sqlite_file_name = "data/selfies_database.db"
        sqlite_url = f"sqlite:///{sqlite_file_name}"

        self.engine = create_engine(sqlite_url, echo=True)

        SQLModel.metadata.create_all(self.engine)


    @command()
    async def polls_to_db(self, ctx):
        print("------------called destructor------------")
        with Session(self.engine) as session:
            print("test1")
            results = session.exec(select(PollDB.poll_id)).all()
            
            for message_id, poll in self.polls.items():
                poll_data = poll.dump_data()
                poll_db = PollDB(
                    poll_id = poll.poll_id,
                    message_id=message_id,
                    poll_data=poll_data.model_dump_json(),
                )
                if poll.poll_id in results:
                    session.exec(update(PollDB).where(PollDB.poll_id == poll.poll_id).values({"poll_id":poll_db.poll_id, "message_id":message_id, "poll_data":poll_db.poll_data})) #type:ignore
                else:  
                    session.add(poll_db)  
            print("test2")
            session.commit()

    @app_commands.command(name='sync', description='Owner only')
    @app_commands.guilds(discord.Object(id=963476559585505360))
    async def sync(self, interaction: discord.Interaction):
        if interaction.user.id == 742425630024400897:
            await self.bot.tree.sync()
            print('Command tree synced.')
        else:
            await interaction.response.send_message('You must be the owner to use this command!')
    
    @command()
    async def sync_apps(self, ctx):
        await self.bot.tree.sync(guild=discord.Object(id=963476559585505360))
    
    
    def _check_if_poll_is_loaded(self, poll_id: int) -> bool:
        return any(poll.poll_id == poll_id for poll in self.current_session_polls.values())

    @Cog.listener(name="on_interaction")
    async def catch_poll_interaction(self, interaction: discord.Interaction):
        if (interaction.type != InteractionType.component):
            print("interaction is not a component interaction")
            return
        if (interaction.data.get('component_type')) != ComponentType.button.value: # type: ignore
            print("interaction component_type is not button.value")
            return
        print(interaction.data)
        _poll_id, _button_type, _button_index = interaction.data.get('custom_id').split(':') # type: ignore
        poll_id: int = int(_poll_id)
        button_type: ButtonType = ButtonType(_button_type)
        button_index: int = int(_button_index)
        if self._check_if_poll_is_loaded(poll_id):
            print("Poll is already loaded")
            return
        else:
            print("test1")
            with Session(self.engine) as session:
                print("test2")
                poll_db = session.get(PollDB, poll_id)
                assert poll_db, "poll not found in database"
                poll_data = PollData.model_validate_json(poll_db.poll_data)
                options_votes_map: dict[int, list[User | Member]] = {option_index: [(member:=interaction.guild.get_member(voter_id)) for voter_id in votes if member] for option_index, votes in poll_data.option_votes_map.items()} #type: ignore
                poll = Poll(
                    poll_id=poll_db.poll_id, #type:ignore
                    title=poll_data.title,
                    author=interaction.guild.get_member(poll_data.author_id), #type: ignore
                    multiple_choice=poll_data.multiple_choice,
                    options=poll_data.options,
                    options_votes_map=options_votes_map,
                    show_results=poll_data.show_results,
                    privacy_button_label=PrivacyButtonText(poll_data.privacy_button_label).value,
                    privacy_button_style=discord.ButtonStyle(poll_data.privacy_button_style),
                )
            print("test3")
            self.polls[poll_db.message_id] = poll
            match button_type:
                case ButtonType.NON_VOTERS:
                    print("test_nonvoters")
                    await poll._show_nonvoters(interaction)
                case ButtonType.PRIVACY:
                    print("test_privacy")
                    await poll._set_privacy(interaction)
                case ButtonType.RESULTS:
                    print("test_results")
                    await poll._get_results(interaction)
                case ButtonType.OPTION_VOTE:
                    print("test_option")
                    await poll._option_button(interaction, button_index)

    @app_commands.command(name="ankieta", description="Stwórz ankietę")
    @app_commands.describe(tytuł="Wybierz tytuł ankiety",
                           typ = "Wybierz typ ankiety",
                           opcja_pierwsza="Określ pierwszą opcję do zagłosowania (maksymalnie 80 znaków!)",
                           opcja_druga = "Określ drugą opcję do zagłosowania (maksymalnie 80 znaków!)",
                           opcja_trzecia = "Określ trzecią opcję do zagłosowania (maksymalnie 80 znaków!)",
                           opcja_czwarta = "Określ czwartą opcję do zagłosowania (maksymalnie 80 znaków!)")
    async def make_poll(self, interaction:discord.Interaction, tytuł:str, typ:PollType, opcja_pierwsza:str, opcja_druga:str, opcja_trzecia:str|None = None, opcja_czwarta:str|None=None):
        options:list[str | None] = [opcja_pierwsza, opcja_druga, opcja_trzecia, opcja_czwarta]
        for option in options:
            if option and len(option) > 80:
                assert isinstance(interaction.channel, TextChannel)
                await interaction.channel.send("Zbyt długi opis opcji (max 80 znaków!)")
        assert isinstance(interaction.user, Member)
        if _check_priviledge(interaction.user, POLLS_PRIVILEDGE_ROLES) or interaction.guild_id == ST_ADMIN_SERVER_ID:
            embed = discord.Embed(title=tytuł)
            poll = Poll(interaction.id, tytuł, interaction.user, True if typ == "Wybór wielokrotny" else False, options)
            await interaction.response.send_message(embed=embed, view=poll)
            message: discord.InteractionMessage = await interaction.original_response()
            message_full_object: discord.Message = await message.fetch()
            message_id: int = message_full_object.id
            self.polls[message_id] = poll #type:ignore
            self.current_session_polls[message_id] = poll #type:ignore
            await message.create_thread(name=f"Dyskusja", auto_archive_duration = 10080)
            



# async def teardown(bot:Bot):
#     polls_cog = bot.get_cog("Polls")
#     assert polls_cog
#     await polls_cog.teardown()

async def setup(bot: Bot):
    print('{:-^50}'.format('loading extension Polls'))
    await bot.add_cog(Polls(bot))







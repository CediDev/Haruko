from functools import partial
from itertools import chain

import discord
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
from discord import Member, TextChannel, User, app_commands
from discord.ext.commands import Bot, Cog


def _check_priviledge(member: discord.Member, priviledged_roles: list[RoleId]) -> bool:
    return bool(set(role.id for role in member.roles) & set(role.value for role in priviledged_roles))


class Poll(discord.ui.View):
    def __init__(
        self,
        title: str,
        author: Member,
        multiple_choice: bool,
        options: list[str | None]
    ) -> None:
        self.multiple_choice: bool = multiple_choice
        self.option_votes_map: dict[int, list[User | Member]]  = {index:[] for index in range(len(options))}
        self.privacy_button_colour: discord.ButtonStyle = discord.ButtonStyle.red
        self.privacy_button_text: PrivacyButtonText = PrivacyButtonText.PRIVATE
        self.author = author
        self.show_results: bool = False
        self.options = options
        self.title: str = title

    @property
    def voters(self) -> list[User | Member]:
        return list(set(chain.from_iterable(
            _voters for _voters in self.option_votes_map.values()
        )))

    async def get_user_votes(self, user_id: int) -> list[int]:
        return [option_index for option_index, votes in self.option_votes_map.items() if user_id in votes]

    async def make_embed(self) -> discord.Embed:
        match self.show_results, self.privacy_button_text:
            case False, PrivacyButtonText.PRIVATE:
                embed = discord.Embed(title=self.title, description=f"Liczba głosów: {len(self.voters)}", color=discord.Colour.pink())
            case False, PrivacyButtonText.PUBLIC:
                raise ValueError("Are you retarded")
            case True, PrivacyButtonText.PRIVATE:
                embed = discord.Embed(title=self.title, description=f"Liczba głosów: {len(self.voters)}", color=discord.Colour.pink())
                for option, votes in zip(self.options, self.option_votes_map.values(), strict=True):
                    if option:
                        embed.add_field(name=f"{FULL_EMOJI} {option}", value="> " + str(len(votes)) + " głosów")
            case True, PrivacyButtonText.PUBLIC:
                embed = discord.Embed(title=self.title, description=f"Liczba głosów: {len(self.voters)}", color=discord.Colour.pink())
                for option, votes in zip(self.options, self.option_votes_map.values(), strict=True):
                    if option:
                        embed.add_field(
                            name=f"{FULL_EMOJI} {option}",
                            value="> " + str(len(votes)) + f" głosów\n{', '.join(user.name for user in votes)}",
                        )
        return embed



    def add_buttons(self):
        async def option_button(interaction:discord.Interaction, index: int):
            votes = await self.get_user_votes(interaction.user.id)
            if index in votes:
                await interaction.response.send_message("Już zagłosowałeś na tę opcję!", ephemeral=True)
                return
            if self.multiple_choice:
                self.option_votes_map[index].append(interaction.user)
                embed = await self.make_embed()
                await interaction.response.edit_message(embeds=[embed], view=self)
                await interaction.followup.send("Pomyślnie oddano głos!", ephemeral=True)
                return
            else:
                self.option_votes_map[index].append(interaction.user)
                if votes:  # non-empty list -> user already voted
                    option_index = votes[0]  # single choice poll means that there is only one vote in votes
                    self.option_votes_map[option_index].remove(interaction.user)
                    await interaction.followup.send("Pomyślnie zmieniono głos!", ephemeral=True)
                else:
                    await interaction.followup.send("Pomyślnie oddano głos!", ephemeral=True)
                embed = await self.make_embed()
                await interaction.response.edit_message(embeds=[embed], view=self)


        privacy_button = discord.ui.Button(label=self.privacy_button_text.value, style=self.privacy_button_colour, row=2)
        async def set_privacy(interaction:discord.Interaction):
            assert isinstance(interaction.user, Member)
            if interaction.user.id == CEDISZ_ID or _check_priviledge(interaction.user, ADMIN_PRIVILEDGE_ROLES):
                self.privacy_button_colour = discord.ButtonStyle.blurple if self.privacy_button_colour == discord.ButtonStyle.red else discord.ButtonStyle.red
                self.privacy_button_text = PrivacyButtonText.PUBLIC if self.privacy_button_text == PrivacyButtonText.PRIVATE else PrivacyButtonText.PRIVATE
                privacy_button.label = self.privacy_button_text.value
                privacy_button.style = self.privacy_button_colour
                embed = await self.make_embed()
                await interaction.response.edit_message(embeds=[embed], view=self)
            else:
                await interaction.response.send_message("Nie masz permisji!", ephemeral=True)
        privacy_button.callback = set_privacy  


        results_button = discord.ui.Button(label="Podaj wyniki", style=discord.ButtonStyle.blurple, row=2)
        async def get_results(interaction:discord.Interaction):
            assert isinstance(interaction.user, Member)
            if interaction.user.id == CEDISZ_ID or interaction.user.id == self.author.id or _check_priviledge(interaction.user, ADMIN_PRIVILEDGE_ROLES):
                self.show_results = not self.show_results  # inverts results visibility setting
                embed = await self.make_embed()
                await interaction.response.edit_message(embeds=[embed], view=self)
            else:
                await interaction.response.send_message("Nie masz permisji!", ephemeral=True)
        results_button.callback = get_results



        nonvoters_visibility_button = discord.ui.Button(label="Niegłosujący", row=2)
        async def show_nonvoters(interaction:discord.Interaction):
            if interaction.guild_id == ST_ADMIN_SERVER_ID:
                assert isinstance(interaction.channel, discord.TextChannel)
                able_to_vote = interaction.channel.members
                nonvoters = [member for member in able_to_vote if member.id not in self.voters and not member.bot]
                message_str = "Brak oddanego głosu: "
                for member in nonvoters:
                    message_str += f"{member.name}, "
                await interaction.response.send_message(message_str, ephemeral=True)
            else:
                await interaction.response.send_message("Nie masz permisji!", ephemeral=True)
        nonvoters_visibility_button.callback = show_nonvoters


        for option_index, option in enumerate(self.options):
            if option:
                button = discord.ui.Button(label=option, style=discord.ButtonStyle.secondary, row=1)
                button.callback = partial(option_button, index = option_index)
                self.add_item(button)

        self.add_item(nonvoters_visibility_button)
        self.add_item(results_button)
        self.add_item(privacy_button)


class Polls(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @app_commands.command(name="ankieta_test", description="Stwórz ankietę")
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
            poll = Poll(tytuł, interaction.user, True if typ == "Wybór wielokrotny" else False, options)
            await interaction.response.send_message(embed=embed, view=poll)


async def setup(bot: Bot):
    await bot.add_cog(Polls(bot))
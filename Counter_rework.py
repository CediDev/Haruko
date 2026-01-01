import discord
from sqlmodel import Field, SQLModel, select, Session, create_engine, update, delete
from constants import CEDISZ_ID, OPIEKUN_KA_SELFIES_ID, Selfies_Channels_IDs
from constants import Selfies_Plus_Points, Selfies_Points
from dataclasses import dataclass
from discord.ext.commands import Cog, Bot, Context, command
from datetime import datetime
import asyncio


@dataclass
class Photo_user:
    user_object: discord.User | discord.Member
    selfies_number: int
    videos_number: int
    points_sum: int

@dataclass
class Photo_channel:
    channel_object: discord.TextChannel
    _users: dict[int, Photo_user] #dict[member.id, photo_user instance] 
    group_photos: list[str] #list[message.jump_url]
    users_without_atencjusz_role: list[int] #list[member.id]


async def is_there_OK(reaction: discord.Reaction) -> bool:
    reaction_givers = [reaction_giver async for reaction_giver in reaction.users()]
    for reaction_giver in reaction_givers:
        if reaction_giver.id == OPIEKUN_KA_SELFIES_ID:
            return True
    return False



class Counter_rework(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        sqlite_file_name = "data/selfies_database.db"
        sqlite_url = f"sqlite:///{sqlite_file_name}"
        self.engine = create_engine(sqlite_url, echo=True)
        SQLModel.metadata.create_all(self.engine)

    
    async def command_maker(self, channel_instance:Photo_channel, author:discord.User | discord.Member) -> None:
        points_list: dict[int, list[int]] = {} #dict[points, list[user_id]]
        match channel_instance.channel_object.id:
            case Selfies_Channels_IDs.SELFIES_PLUS_CHANNEL_ID.value:
                points_for_selfie = Selfies_Plus_Points.SELFIE.value
                points_for_video = Selfies_Plus_Points.VIDEO.value
            case Selfies_Channels_IDs.SELFIES_CHANNEL_ID.value:
                points_for_selfie = Selfies_Points.SELFIE.value
                points_for_video = Selfies_Points.VIDEO.value
        for user in Photo_channel._users.values():
            user.points_sum = (points_for_selfie * user.selfies_number) + (points_for_video * user.videos_number)
            if user.points_sum not in points_list:
                points_list[user.points_sum] = []
            points_list[user.points_sum].append(user.user_object.id)
        for points_value, list_of_users_ids in points_list.items():
            command_string = f".punkty-dodaj {points_value}"
            for user_id in list_of_users_ids:
                command_string = command_string + f" <@{user_id}>"
            await author.send(content = "`"+command_string+"`"+f"Punkty za {channel_instance.channel_object.name}") #type:ignore
            await self.bot.get_channel(Selfies_Channels_IDs.SELFIES_RAPORT_CHANNEL_ID.value).send(content = "`"+command_string+"`"+f"Punkty za {channel_instance.channel_object.name}") #type:ignore
            await asyncio.sleep(2)


    @command()
    async def count_selfies(self, ctx: Context, starting_date: str, ending_date: str) -> None:
        if not ctx.author.id == OPIEKUN_KA_SELFIES_ID or ctx.author.id == CEDISZ_ID:
            return
        start_day, start_month, start_year = [int(i) for i in starting_date.split("-")]
        end_day, end_month, end_year = [int(i) for i in ending_date.split("-")]
        atencjusz_role_object = discord.utils.get(ctx.guild.roles, name="Atencjusz") #type:ignore
        photo_channels = {
            "selfies_channel": Photo_channel(
                channel_object = self.bot.get_channel(SELFIES_CHANNEL_ID), #type:ignore
                _users = {},
                group_photos = [],
                users_without_atencjusz_role = [],
            ),
            "selfies_plus_channel": Photo_channel(
                channel_object = self.bot.get_channel(SELFIES_PLUS_CHANNEL_ID), #type:ignore
                _users = {},
                group_photos = [],
                users_without_atencjusz_role = [],
            )
        }
        for photo_channel in photo_channels.values():
            async for message in photo_channel.channel_object.history(
                limit=5000,
                after=datetime(start_year, start_month, start_day),
                before=datetime(end_year, end_month, end_day)
            ):
                forced_continue = False
                message_author_object = ctx.guild.get_member(message.author.id) #type:ignore
                if not message_author_object: continue
                for reaction in message.reactions:
                    if reaction.emoji == "❌":
                        if await is_there_OK(reaction):
                            forced_continue = not forced_continue
                            break
                if forced_continue: continue
                if message_author_object.id not in photo_channel._users:    
                    photo_channel._users[message_author_object.id] = Photo_user(
                        user_object = message_author_object,
                        selfies_number = 0,
                        videos_number = 0,
                        points_sum = 0
                    )
                if atencjusz_role_object not in message_author_object.roles:
                    photo_channel.users_without_atencjusz_role.append(message_author_object.id)
                photo_channel._users[message_author_object.id].selfies_number += 1
                for reaction in message.reactions:
                    match reaction.emoji:
                        case "🎬":
                            if is_there_OK(reaction):
                                photo_channel._users[message_author_object.id].videos_number += 1
                                photo_channel._users[message_author_object.id].selfies_number -= 1
                                continue
                        case "🎀":
                            if is_there_OK(reaction):
                                photo_channel.group_photos.append(message.jump_url)
                                photo_channel._users[message_author_object.id].selfies_number -= 1
                                continue
                        case "2️⃣":
                            if is_there_OK(reaction):
                                photo_channel._users[message_author_object.id].selfies_number += 1
                                continue
                        case "3️⃣":
                            if is_there_OK(reaction):
                                photo_channel._users[message_author_object.id].selfies_number += 2
                                continue                
            await Counter_rework.command_maker(self, photo_channel, ctx.author)
            


async def setup(bot: Bot):
    await bot.add_cog(Counter_rework(bot))

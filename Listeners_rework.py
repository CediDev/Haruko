import discord
from sqlmodel import Field, SQLModel, select, Session, create_engine, update, delete
from constants import CEDISZ_ID, OPIEKUN_KA_SELFIES_ID, Selfies_Channels_IDs, Other_Photo_Channels_IDs, ANNO_BOARD_CHANNEL_ID, SZUKAM_ZNAJOMYCH_CHANNEL_ID
from dataclasses import dataclass
from discord.ext.commands import Cog, Bot, Context, command
from datetime import datetime
import asyncio



class BirthdayUserData(SQLModel, table=True):
    user_id: int | None = Field(default=None, primary_key=True)
    selfies_number: int
    pupile_photos_number: int
    kuchnia_photos_number: int
    niesforne_photos_number: int 
    counter_file: str = Field(default="count_basic.png")
    likes_count: int



class Listeners_rework(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        sqlite_file_name = "data/selfies_database.db"
        sqlite_url = f"sqlite:///{sqlite_file_name}"
        self.engine = create_engine(sqlite_url, echo=True)
        SQLModel.metadata.create_all(self.engine)


    #@Cog.listener("on_message")
    #async def adding_user_to_database(self, message:discord.Message):


    @Cog.listener("on_message")
    async def photo_channels_thread_creator(self, message:discord.Message):
        if message.author.bot:
            return
        match message.channel.id:
            case Other_Photo_Channels_IDs.KUCHNIA_CHANNEL_ID.value:
                await message.create_thread(name=f"Komentarze: {message.author.name}", auto_archive_duration = 10080)
            case Other_Photo_Channels_IDs.NIESFORNE_CHANNEL_ID.value:
                await message.create_thread(name=f"Komentarze: {message.author.name}", auto_archive_duration = 10080)
            case Selfies_Channels_IDs.SELFIES_CHANNEL_ID.value:
                await message.create_thread(name=f"Komentarze: {message.author.name}", auto_archive_duration = 10080)
            case Selfies_Channels_IDs.SELFIES_PLUS_CHANNEL_ID.value:
                await message.create_thread(name=f"Komentarze: {message.author.name}", auto_archive_duration = 10080)


    @Cog.listener("on_message")
    async def tablica_ogloszen_thread_creator(self, message:discord.Message):
        if message.author.bot:
            return
        if message.channel.id == ANNO_BOARD_CHANNEL_ID:
            await message.create_thread(name=f"Skomentuj!", auto_archive_duration=10080)


    @Cog.listener("on_message")
    async def szukam_znajomych_thread_creator(self, message:discord.Message):
        if message.author.bot:
            return
        if message.channel.id == SZUKAM_ZNAJOMYCH_CHANNEL_ID:
            await message.create_thread(name=f"Napisz do {message.author.name}!", auto_archive_duration=10080)
    

    @Cog.listener("on_message")
    async def przywitaj_się_thread_creator(self, message:discord.Message):
        welcome_channel = self.bot.get_channel(412202170549796874)
        if message.channel.id == welcome_channel.id and not message.author.bot:
            await message.create_thread(name="Witamy w naszych progach!!! ♡", auto_archive_duration=1440)


async def setup(bot: Bot):
    print('{:-^50}'.format('loading extension Polls'))
    await bot.add_cog(Listeners_rework(bot))
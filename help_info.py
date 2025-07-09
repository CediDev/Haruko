from discord.ext.commands import Bot
import matplotlib
import discord
import asyncio
import datetime
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from discord.ext.commands import Cog, Bot, command
import sqlite3
from pathlib import Path, PurePath
import os
from discord.ext import tasks
import time as t
from zoneinfo import ZoneInfo
from discord import app_commands
from typing import Literal

con = sqlite3.connect('data/selfies_database.db')
con.row_factory = sqlite3.Row
cur = con.cursor()

class help_info(Cog):
    
    intents = discord.Intents.all()
    intents.message_content = True
    intents.members = True
    intents.guilds = True
    
    def __init__(self, bot: Bot):
        self.bot = bot

    
    @command()
    async def mess_stats(ctx, self, starting_month, ending_month):
        selfies_channel = self.bot.get_channel(412146947412197396)
        async for message in selfies_channel.history():
            pass

from discord.ext.commands import Bot
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


class reload(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @app_commands.command(name="reload", description="Komenda do reloadowania funkcji")
    @app_commands.describe(module = "Wybierz plik")
    async def _reload(self, interaction:discord.Interaction, module: Literal["economy_ex","counter_ex","polls","ShopViewer","listeners_tasks","questy","database_making","gambling","addon", "message_reminder"]):
        if interaction.user.id == 742425630024400897:
            try:
                await self.bot.unload_extension(module)
                await self.bot.load_extension(module)
                await interaction.response.send_message(f'{module} reloaded')
            except Exception as e:
                await interaction.response.send_message("Coś poszło nie tak")
                await interaction.followup.send('{}: {}'.format(type(e).__name__, e))

    @app_commands.command(name="load", description="Komenda do loadowania funkcji")
    @app_commands.describe(module = "Wybierz plik")
    async def _load(self, interaction:discord.Interaction, module: Literal["economy_ex","counter_ex","polls","ShopViewer","listeners_tasks","questy","database_making","gambling","addon", "message_reminder"]):
        if interaction.user.id == 742425630024400897:
            try:
                await self.bot.load_extension(module)
                await interaction.response.send_message(f'{module} loaded')
            except Exception as e:
                await interaction.response.send_message("Coś poszło nie tak")
                await interaction.followup.send('{}: {}'.format(type(e).__name__, e))

    @app_commands.command(name="reloadall", description="reloading wszystkiego naraz")
    async def _reloadall(self, interaction:discord.Interaction):
        if interaction.user.id == 742425630024400897:
            try:
                await self.bot.unload_extension("economy_ex")
                await self.bot.unload_extension("counter_ex")
                await self.bot.unload_extension("polls")
                #await self.bot.unload_extension("ShopViewer")
                await self.bot.unload_extension("listeners_tasks")
                await self.bot.unload_extension("questy")
                #await self.bot.unload_extension("database_making")
                await self.bot.unload_extension("gambling")
                await self.bot.unload_extension("reload")
                await self.bot.unload_extension("addon")
                
                await self.bot.load_extension("economy_ex")
                await self.bot.load_extension("counter_ex")
                await self.bot.load_extension("polls")
                #await self.bot.load_extension("ShopViewer")
                await self.bot.load_extension("listeners_tasks")
                await self.bot.load_extension("questy")
                #await self.bot.load_extension("database_making")
                await self.bot.load_extension("gambling")
                await self.bot.load_extension("reload")
                await self.bot.load_extension("addon")
                
                await interaction.response.send_message(f'Reload zakończony sukcesem')
            except Exception as e:
                await interaction.response.send_message("Coś poszło nie tak")
                await interaction.followup.send('{}: {}'.format(type(e).__name__, e))


async def setup(bot: Bot):
    await bot.add_cog(reload(bot))
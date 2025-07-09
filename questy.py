from discord.ext.commands import Cog, Bot, command
import discord
import sqlite3
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os
import matplotlib.pyplot as plt
import numpy as np
import random
from discord import app_commands
from discord.ext import tasks
from typing import Literal
import time as t
import asyncio
import datetime
from pathlib import Path, PurePath


class questy(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @app_commands.command(
        name="quest", description="Tworzy questa z danym terminem, nagrodą oraz opisem."
    )
    @app_commands.describe(
        termin="Sprecyzuj termin",
        nagroda="Opisz nagrodę możliwą do zdobycia",
        opis="Opisz na czym ma polegać quest",
    )
    async def schedule(
        self, interaction: discord.Interaction, termin: str, nagroda: str, opis: str
    ):
        if interaction.user.id == 742425630024400897:
            raport_channel = self.bot.get_channel(1188542888989163620)
            date = t.strftime("%Y-%m-%d %H:%M")
            channel_to_send = self.bot.get_channel(494895117006667797)
            full_emoji = discord.utils.get(self.bot.emojis, name="arrow_right")
            ID = str(random.randint(0, 9))
            for i in range(0, 9):
                ID = ID + str(random.randint(0, 9))
            e = discord.Embed(
                title="Queścik!",
                description=f"ID zadania: {ID}",
                colour=discord.Colour.pink(),
            )
            e.add_field(name=f"", value=f"{full_emoji} *{opis}*")
            e.add_field(name=f"Nagroda: `{nagroda}`", value="", inline=False)
            e.set_footer(text=f"Termin: {termin}")
            await interaction.response.send_message(
                f"Quest ID: {ID} został utworzony!", ephemeral=True
            )
            await raport_channel.send(
                f"{date} | {interaction.user.name} utworzył Questa:", embed=e
            )
            await channel_to_send.send(embed=e)
        else: 
            interaction.response.send_message("Nie masz permisji", ephemeral=True)

    @app_commands.command(
        name="apply", description="Wysyła zgłoszenie na konkretnego questa!"
    )
    @app_commands.describe(
        id="Wklej ID questa, do którego się zgłaszasz",
        link="Wklej link do zdjęcia/wiadomości, które chcesz zgłosić",
    )
    async def quescik(self, interaction: discord.Interaction, id: str, link: str):
        raport_channel = self.bot.get_channel(1188542888989163620)
        date = t.strftime("%Y-%m-%d %H:%M")
        channel_to_send = self.bot.get_channel(1179884652522115102)
        await interaction.response.send_message(
            "Zgłoszenie wysłane ;333", ephemeral=True
        )
        await channel_to_send.send(f"{interaction.user.name} | ID questa: {id}\n{link}")
        await raport_channel.send(
            f"{date} | {interaction.user.name} wysłał zgłoszenie do Questa | ID: {id} | Link do zgłoszenia: {link}"
        )


async def setup(bot: Bot):
    await bot.add_cog(questy(bot))

import discord
from discord.ext.commands import Bot
import logging
import discord
import asyncio
from discord.ext import commands

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
import re




logging.basicConfig(level="INFO")

intents = discord.Intents.all()
intents.message_content = True
intents.members = True

if "BOT_TOKEN" in os.environ:
    token = os.environ["BOT_TOKEN"]
else:
    with open("TOKEN.txt") as f:
        token = f.read().strip()
    
async def main():


    bot = Bot(
        command_prefix="s!", intents=intents, activity=discord.Game(name="Liczę..."))
    bot.polls_instances_list = []    
    bot.mess_reminder_instances_list = []
    bot.remove_command("help")
    await bot.load_extension("economy_ex")
    await bot.load_extension("counter_ex")
    await bot.load_extension("Polls")
    await bot.load_extension("instances_archive")
    await bot.load_extension("listeners_tasks")
    await bot.load_extension("questy")
    await bot.load_extension("message_reminder")
    await bot.load_extension("reload")
    await bot.load_extension("birthday")
    #await bot.load_extension("addon")
    await bot.start(token=token)
    

async def cleanup():
    print("Cleaning up before shutdown...")
    # Perform any necessary cleanup here
    await asyncio.sleep(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        print("Received exit signal, shutting down...")
        asyncio.run(cleanup())

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        print("Cleanup complete. Exiting.")

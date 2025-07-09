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
from zoneinfo import ZoneInfo



class instances_archive(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.instances_list = []
        self.instances_temp_list = []



async def setup(bot: Bot):
    await bot.add_cog(instances_archive(bot))

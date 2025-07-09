from discord.ext.commands import Cog, Bot, command
import discord
from discord import app_commands
from discord.ext import tasks
from typing import Literal
import time as t
import asyncio
import datetime
from pathlib import Path, PurePath
from zoneinfo import ZoneInfo



reminder_hours = [datetime.time(hour=6,tzinfo=ZoneInfo("Europe/Warsaw")),
                  datetime.time(hour=12,tzinfo=ZoneInfo("Europe/Warsaw")),
                  datetime.time(hour=18,tzinfo=ZoneInfo("Europe/Warsaw")),
                  datetime.time(hour=23,minute=59,tzinfo=ZoneInfo("Europe/Warsaw"))]


class message_reminder(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    class reminder_button(discord.ui.View):
        def __init__(self,bot: Bot, interaction_channel, author, message):
            self.bot = bot
            self.user_list:list = []
            self.admin_color = discord.ButtonStyle.red
            self.channel = interaction_channel
            self.author = author
            self.message = message
            super().__init__(timeout=None)
            self.add_button()


        def add_button(self):
            confirm_butt = discord.ui.Button(label="Potwierdź", row = 1)
            async def confirm_button(interaction: discord.Interaction):
                if "`"+str(interaction.user.name)+"`" not in self.user_list:
                    self.lists[0].append("`"+str(interaction.user.name)+"`")
                    self.overall_list.append(interaction.user)
                    await interaction.followup.send("Potwierdzono zapoznanie się z wiadomością!", ephemeral=True)
                elif "`"+interaction.user.name+"`" in self.user_list:
                    await interaction.response.send_message("Już potwierdziłeś zapoznanie się z wiadomością!", ephemeral=True)
            confirm_butt.callback = confirm_button
            self.add_item(confirm_butt)

    @app_commands.command(name="potwierdzenie", description="Reminder do zapoznania się z wiad.")
    @app_commands.describe(message="ID do wiadomości")
    async def mess_reminder_func(self, interaction:discord.Interaction, message:int):
        if interaction.guild.id == 1198978337150881812 or interaction.guild.id == 963476559585505360:
            instance = message_reminder.reminder_button(self, self.bot, interaction.channel, interaction.user, message)
            message_object = await interaction.channel.fetch_message(message)
            self.bot.mess_reminder_instances_list.append([instance, 0])
            await interaction.response.send_message(content=f"Cześć, {interaction.user.name} prosi o zapoznanie się z wiadomością - {message_object.jump_url}. Gdy to zrobisz, odznacz ten fakt przyciskiem poniżej.", view=instance)
        

    
    async def find_nonvoters(ctx, self, poll_instance) -> list:
        available_to_vote = poll_instance.channel.members[:50]
        users_converted_to_members = [poll_instance.channel.guild.get_member(ThreadMember.id) for ThreadMember in available_to_vote]
        nonvoters = [member for member in users_converted_to_members if (member not in poll_instance.overall_list and not member.bot)]
        return nonvoters


    @tasks.loop(time=reminder_hours)
    async def mess_reminder(ctx, self):
        temp_instances_list = []
        for polls_instance in self.bot.mess_reminder_instances_list:
            instance = polls_instance[0]
            turn = polls_instance[1]
            if turn <= 8:
                temp_instances_list.append(polls_instance)
                continue
        for polls_instance in temp_instances_list:
            nonvoters_list = [member.mention for member in await message_reminder.find_nonvoters(ctx, self, instance)]
            if len(nonvoters_list) < 1:
                continue
            nonvoters_str =", ".join(nonvoters_list)
            await instance.channel.send(nonvoters_str + "\nHej, przypominam o zapoznaniu się z wiadomością: " + polls_instance.message)
            polls_instance[2] += 1    
        self.bot.mess_reminder_instances_list = temp_instances_list

    @command()
    async def mes_reminder_start(ctx, self):
        if self.author.id == 742425630024400897:
            message_reminder.mess_reminder.start(ctx, self)
            print("done")
    
    @command()
    async def mes_reminder_stop(ctx, self):
        if self.author.id == 742425630024400897:
            message_reminder.nonvoters_reminder.cancel()
            print("done")



async def setup(bot: Bot):
    await bot.add_cog(message_reminder(bot))





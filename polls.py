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

instances_list = []

class polls(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot


    
    class pollsButtons(discord.ui.View):
        def __init__(self,bot: Bot, multiple_choice, title, interaction_channel, author, option1, option2=None, option3=None, option4=None):
            self.bot = bot
            self.title = title
            self.overall_list = []
            self.status = True
            self.admin_color = discord.ButtonStyle.red
            self.admin_text = "Prywatne"
            self.multiple_choice = multiple_choice
            self.podaj_wyniki = False
            self.channel = interaction_channel
            self.author = author

            self.pre_options = [option1, option2, option3, option4]
            self.options = [option for option in self.pre_options if option]

            self.lists = [[] for option in self.pre_options if option]
            
            super().__init__(timeout=None)
            self.add_buttons()
        
        def nicks_string_maker(self, nicks):
            text = ', '.join(nicks)
            return text

        async def embed_maker(self, num, stat=None):
            if self.podaj_wyniki == False and self.admin_text == "Prywatne" and stat is None:
                s_embed = discord.Embed(
                    title=self.title,
                    description=f"{full_emoji} Liczba głosów: {len([vote for list_of_votes in self.lists for vote in list_of_votes])}",
                    colour=discord.Colour.pink(),
                )
                return s_embed
            if stat is None:
                stat = self.status
            s_embed = discord.Embed(title=self.title, colour=discord.Colour.pink())
            nicks = {
                index: polls.pollsButtons.nicks_string_maker(self, self.lists[index])
                for index in range(len(self.lists))
            }

            for index in range(num):
                if stat is False:
                    value = f"> {len(self.lists[index])} głosów\n{nicks[index]}"
                else:
                    value = f"> {len(self.lists[index])} głosów"
                s_embed.add_field(
                    name=f"{full_emoji} {self.pre_options[index]}", value=value,
                )

            return s_embed
            
       
        async def other_options_checker(self, nickname, option):
            for index, list_of_votes in enumerate(self.lists):
                if nickname in list_of_votes and option != index:
                    return [list_of_votes, self.pre_options[index]]
            return False

        
        def add_buttons(self):
            
            buttons_dict = {}
            for x, option_id in enumerate([option for option in self.pre_options if option]):
                buttons_dict[x] = discord.ui.Button(label=str(option_id), style=discord.ButtonStyle.secondary, row = 1)

            
            async def button_one(interaction: discord.Interaction):
                status = await polls.pollsButtons.other_options_checker(self, "`"+interaction.user.name+"`", 0)
                if self.multiple_choice == "multi":
                    if "`"+str(interaction.user.name)+"`" not in self.lists[0]:
                        self.lists[0].append("`"+str(interaction.user.name)+"`")
                        self.overall_list.append(interaction.user)
                        embed_s = await polls.pollsButtons.embed_maker(self, len(buttons_dict))                     
                        await interaction.response.edit_message(embeds= [embed_s], view=self, )
                        await interaction.followup.send("Pomyślnie oddano głos!", ephemeral=True)
                        await polls.pollsButtons.archiver(self, buttons_dict)
                    elif "`"+interaction.user.name+"`" in self.lists[0]:await interaction.response.send_message("Już zagłosowałeś na tę opcję!", ephemeral=True)
                elif status == False and self.multiple_choice == "single":
                    if interaction.user not in self.overall_list:
                        self.lists[0].append("`"+str(interaction.user.name)+"`")
                        self.overall_list.append(interaction.user)
                        embed_s = await polls.pollsButtons.embed_maker(self, len(buttons_dict))                     
                        await interaction.response.edit_message(embeds= [embed_s], view=self, )
                        await interaction.followup.send("Pomyślnie oddano głos!", ephemeral=True)
                        await polls.pollsButtons.archiver(self, buttons_dict)
                    else:
                        await interaction.response.send_message("Już zagłosowałeś na tę opcję!", ephemeral=True)
                elif status != False and self.multiple_choice == "single":
                    status[0] = status[0].remove("`"+str(interaction.user.name)+"`")
                    self.lists[0].append("`"+str(interaction.user.name)+"`")
                    embed_s = await polls.pollsButtons.embed_maker(self, len(buttons_dict))                    
                    await interaction.response.edit_message(embeds=[ embed_s], view=self, )
                    await interaction.followup.send(ephemeral=True, content="Zmieniono Twój głos")
                    await polls.pollsButtons.archiver(self, buttons_dict)
            buttons_dict[0].callback = button_one
            
            
            async def button_two(interaction: discord.Interaction):
                status = await polls.pollsButtons.other_options_checker(self, "`"+interaction.user.name+"`", 1)
                if self.multiple_choice == "multi":
                    if "`"+interaction.user.name+"`" not in self.lists[1]:
                        self.lists[1].append("`"+str(interaction.user.name)+"`")
                        self.overall_list.append(interaction.user)
                        embed_s = await polls.pollsButtons.embed_maker(self, len(buttons_dict))                      
                        await interaction.response.edit_message(embeds= [embed_s], view=self, )
                        await interaction.followup.send("Pomyślnie oddano głos!", ephemeral=True)
                        await polls.pollsButtons.archiver(self, buttons_dict)
                    elif "`"+interaction.user.name+"`" in self.lists[1]:await interaction.response.send_message("Już zagłosowałeś na tę opcję!", ephemeral=True)
                elif status == False and self.multiple_choice == "single":
                    if interaction.user not in self.overall_list:
                        self.lists[1].append("`"+str(interaction.user.name)+"`")
                        self.overall_list.append(interaction.user)
                        embed_s= await polls.pollsButtons.embed_maker(self, len(buttons_dict))                       
                        await interaction.response.edit_message(embeds= [embed_s], view=self,)
                        await interaction.followup.send("Pomyślnie oddano głos!", ephemeral=True)
                        await polls.pollsButtons.archiver(self, buttons_dict)
                    else:
                        await interaction.response.send_message("Już zagłosowałeś na tę opcję!", ephemeral=True)
                elif status != False and self.multiple_choice == "single":
                    status[0] = status[0].remove("`"+str(interaction.user.name)+"`")
                    self.lists[1].append("`"+str(interaction.user.name)+"`")
                    embed_s = await polls.pollsButtons.embed_maker(self, len(buttons_dict))                 
                    await interaction.response.edit_message(embeds=[ embed_s], view=self, )
                    await interaction.followup.send(ephemeral=True, content="Zmieniono Twój głos")
                    await polls.pollsButtons.archiver(self, buttons_dict)
            buttons_dict[1].callback = button_two

            if len(buttons_dict) >= 3:
                async def button_three(interaction: discord.Interaction):
                    status = await polls.pollsButtons.other_options_checker(self, "`"+interaction.user.name+"`", 2)
                    if self.multiple_choice == "multi":
                        if "`"+interaction.user.name+"`" not in self.lists[2]:
                            self.lists[2].append("`"+str(interaction.user.name)+"`")
                            self.overall_list.append(interaction.user)
                            embed_s= await polls.pollsButtons.embed_maker(self, len(buttons_dict))                         
                            await interaction.response.edit_message(embeds= [embed_s], view=self,)
                            await interaction.followup.send("Pomyślnie oddano głos!", ephemeral=True)
                            await polls.pollsButtons.archiver(self, buttons_dict)
                        elif "`"+interaction.user.name+"`" in self.lists[2]:await interaction.response.send_message("Już zagłosowałeś na tę opcję!", ephemeral=True)
                    elif status == False and self.multiple_choice == "single":
                        if interaction.user not in self.overall_list:
                            self.lists[2].append("`"+str(interaction.user.name)+"`")
                            self.overall_list.append(interaction.user)
                            embed_s = await polls.pollsButtons.embed_maker(self, len(buttons_dict))
                            
                            await interaction.response.edit_message(embeds= [embed_s], view=self, )
                            await interaction.followup.send("Pomyślnie oddano głos!", ephemeral=True)
                            await polls.pollsButtons.archiver(self, buttons_dict)
                        else:
                            await interaction.response.send_message("Już zagłosowałeś na tę opcję!", ephemeral=True)
                    elif status != False and self.multiple_choice == "single":
                        status[0] = status[0].remove("`"+str(interaction.user.name)+"`")
                        self.lists[2].append("`"+str(interaction.user.name)+"`")
                        embed_s = await polls.pollsButtons.embed_maker(self, len(buttons_dict))
                        await interaction.response.edit_message(embeds=[ embed_s], view=self, )
                        await interaction.followup.send(ephemeral=True, content="Zmieniono Twój głos")
                        await polls.pollsButtons.archiver(self, buttons_dict)
                buttons_dict[2].callback = button_three

        
            if len(buttons_dict) == 4:   
                async def button_four(interaction: discord.Interaction):
                    status = await polls.pollsButtons.other_options_checker(self, "`"+interaction.user.name+"`", 3)
                    if self.multiple_choice == "multi":
                        if "`"+interaction.user.name+"`" not in self.lists[3]:
                            self.lists[3].append("`"+str(interaction.user.name)+"`")
                            self.overall_list.append(interaction.user)
                            embed_s = await polls.pollsButtons.embed_maker(self, len(buttons_dict))                       
                            await interaction.response.edit_message(embeds= [embed_s], view=self, )
                            await interaction.followup.send("Pomyślnie oddano głos!", ephemeral=True)
                            await polls.pollsButtons.archiver(self, buttons_dict)
                        elif "`"+interaction.user.name+"`" in self.lists[3]:await interaction.response.send_message("Już zagłosowałeś na tę opcję!", ephemeral=True)
                    elif status == False and self.multiple_choice == "single":
                        if interaction.user not in self.overall_list:
                            self.lists[3].append("`"+str(interaction.user.name)+"`")
                            self.overall_list.append(interaction.user)
                            embed_s = await polls.pollsButtons.embed_maker(self, len(buttons_dict))                             
                            await interaction.response.edit_message(embeds= [embed_s], view=self,)
                            await interaction.followup.send("Pomyślnie oddano głos!", ephemeral=True)
                            await polls.pollsButtons.archiver(self, buttons_dict)
                        else:
                            await interaction.response.send_message("Już zagłosowałeś na tę opcję!", ephemeral=True)
                    elif status != False and self.multiple_choice == "single":
                        status[0] = status[0].remove("`"+str(interaction.user.name)+"`")
                        self.lists[3].append("`"+str(interaction.user.name)+"`")
                        embed_s = await polls.pollsButtons.embed_maker(self, len(buttons_dict))
                        await interaction.response.edit_message(embeds=[ embed_s], view=self,)
                        await interaction.followup.send(ephemeral=True, content="Zmieniono Twój głos")
                        await polls.pollsButtons.archiver(self, buttons_dict)
                buttons_dict[3].callback = button_four
            



            
            private_public_button = discord.ui.Button(label=self.admin_text, style=self.admin_color, row = 2)
            async def button_admin(interaction: discord.Interaction):
                if (ST_role in interaction.user.roles or ST_server_admin_role in interaction.user.roles or interaction.user.guild_permissions.administrator == True or interaction.user.id == 397329204867235842):
                    if self.status == True:
                        self.status = False
                    elif self.status == False:
                        self.status = True

                    if self.admin_color == discord.ButtonStyle.blurple:
                        self.admin_color = discord.ButtonStyle.red
                    elif self.admin_color == discord.ButtonStyle.red:
                        self.admin_color = discord.ButtonStyle.blurple

                    if self.admin_text == "Publiczne":
                        self.admin_text = "Prywatne"
                    elif self.admin_text == "Prywatne":
                        self.admin_text = "Publiczne"

                    private_public_button.style = self.admin_color
                    private_public_button.label = self.admin_text
                    
                    embed_s= await polls.pollsButtons.embed_maker(self, len(buttons_dict))
                    
                    
                    
                    await interaction.response.edit_message(embeds= [embed_s], view=self, )
                else:
                    await interaction.response.send_message("Nie masz permisji!", ephemeral=True)
            private_public_button.callback = button_admin

            
            wyniki_button = discord.ui.Button(label="Podaj wyniki", style = discord.ButtonStyle.blurple, row = 2)
            async def button_wyniki(interaction:discord.Interaction):
                if (interaction.user.id == self.author.id or interaction.user.id == 397329204867235842 or ST_role in interaction.user.roles or interaction.user.guild_permissions.administrator == True):
                        if self.podaj_wyniki == False:
                            self.podaj_wyniki = True
                        elif self.podaj_wyniki == True:
                            self.podaj_wyniki = False
                        embed_s= await polls.pollsButtons.embed_maker(self, len(buttons_dict))
                        
                        await interaction.response.edit_message(embeds= [embed_s], view=self, )
                elif interaction.guild.id != 211261411119202305 and interaction.guild.id != 963476559585505360:
                    if (SMA_role in interaction.user.roles or ST_server_admin_role in interaction.user.roles or interaction.user.guild_permissions.administrator==True or interaction.user.id == 397329204867235842):
                        if self.podaj_wyniki == False:
                            self.podaj_wyniki = True
                        elif self.podaj_wyniki == True:
                            self.podaj_wyniki = False
                        embed_s= await polls.pollsButtons.embed_maker(self, len(buttons_dict))
                        
                        await interaction.response.edit_message(embeds= [embed_s], view=self, )
                else:
                        await interaction.response.send_message("Nie masz permisji", ephemeral=True)
            
            wyniki_button.callback = button_wyniki

            
            nonvoters_button = discord.ui.Button(label="Niegłosujący", row = 2)
            async def button_nonvoters(interaction: discord.Interaction):
                print(interaction.user.name)
                print(interaction.user.roles)
                if (interaction.user.id == self.author.id and ST_role in interaction.user.roles) or (interaction.user.id == self.author.id and ST_role_ST_server in interaction.user.roles) or SMA_plus_role in interaction.user.roles or interaction.user.id == 397329204867235842 or interaction.user.id == 742425630024400897:
                    available_to_vote = self.channel.members
                    users_converted_to_members = [interaction.guild.get_member(ThreadMember.id) for ThreadMember in available_to_vote]
                    nonvoters = [member for member in users_converted_to_members if (member not in self.overall_list and not member.bot)]
                    message_str = "Brak oddanego głosu: "
                    for member in nonvoters:
                        message_str += f"{member.mention}, "
                    await interaction.response.send_message(message_str, ephemeral=True)
                else:
                    await interaction.response.send_message("Nie masz permisji.", ephemeral=True)
            
            nonvoters_button.callback = button_nonvoters



            for button in buttons_dict.items():
                button_to_add = button[1]
                self.add_item(button_to_add)
            
            self.add_item(private_public_button)
            self.add_item(wyniki_button)
            self.add_item(nonvoters_button)
            

        async def archiver(self, buttons_dict):
            await archive_channel.send(embeds=[await polls.pollsButtons.embed_maker(self, len(buttons_dict), False)])

    
    
    @app_commands.command(name="ankieta", description="Komenda tworząca ankiety")
    @app_commands.describe(tytuł="Wybierz tytuł ankiety", 
                           typ = "Wybierz typ ankiety",
                           opcja_pierwsza="Określ pierwszą opcję do zagłosowania (maksymalnie 80 znaków!)",
                           opcja_druga = "Określ drugą opcję do zagłosowania (maksymalnie 80 znaków!)",
                           opcja_trzecia = "Określ trzecią opcję do zagłosowania (maksymalnie 80 znaków!)",
                           opcja_czwarta = "Określ czwartą opcję do zagłosowania (maksymalnie 80 znaków!)")
    async def schedule(self, interaction: discord.Interaction, tytuł:str, typ:Literal["single", "multi"], opcja_pierwsza:str, opcja_druga:str, opcja_trzecia:str = None, opcja_czwarta:str = None):
        global full_emoji, OK_role, ST_role, OE_role, AA_role, ST_server_admin_role, SMA_role, archive_channel, SMA_plus_role, ST_role_ST_server
        options = [opcja_pierwsza, opcja_druga, opcja_trzecia, opcja_czwarta]
        for option in options:
            if option != None:
                if len(option) > 80:
                    await interaction.channel.send("Zmniejsz ilość znaków na przyciskach (max 80).")
                    return _
        OK_role = discord.utils.get(interaction.guild.roles, id = 412193755286732800)
        ST_role = discord.utils.get(interaction.guild.roles, id= 303943612784181248)
        ST_role_ST_server = discord.utils.get(interaction.guild.roles, id=1198978337176035464)
        OE_role = discord.utils.get(interaction.guild.roles, id= 422408722107596811)
        AA_role = discord.utils.get(interaction.guild.roles, id = 1200031170012909629)
        SMA_role = discord.utils.get(interaction.guild.roles, id=1198978337217970285)
        SMA_plus_role = discord.utils.get(interaction.guild.roles, id=1198978337217970286)
        ST_server_admin_role = discord.utils.get(interaction.guild.roles, id=1198978337247350794)
        archive_channel = self.bot.get_channel(1211268323875102820)
        if OK_role in interaction.user.roles or OE_role in interaction.user.roles or ST_role in interaction.user.roles or AA_role in interaction.user.roles or interaction.guild_id != 211261411119202305:
            full_emoji = discord.utils.get(self.bot.emojis, name="arrow_right")
            main_embed = discord.Embed(title=tytuł)
            polls_instance = polls.pollsButtons(self,typ, tytuł, interaction.channel, interaction.user, opcja_pierwsza, opcja_druga, opcja_trzecia, opcja_czwarta)
            await interaction.response.send_message(embed= main_embed,view=polls_instance)
            if interaction.guild.id == 1198978337150881812 or interaction.guild.id == 963476559585505360:
                poll_message:discord.Message = await interaction.original_response()
                self.bot.polls_instances_list.append([polls_instance, poll_message, 0])
                #polls.info_share.start(self, polls_instance, poll_message, interaction.channel)
                #await asyncio.sleep(86400)
                await asyncio.sleep(86400)
                nonvoters = await polls.find_nonvoters(self, polls_instance)
                string_of_wyniki = ""
                for i,n in enumerate(polls_instance.options, start=0):
                    print(i)
                    string_of_wyniki += f"\n{n} : {len(polls_instance.lists[i])}" 
                await interaction.channel.send(f"{polls_instance.author.mention}, oto wyniki Twojej ankiety:{string_of_wyniki}\n\nBrak głosu: {nonvoters}", reference=poll_message)
        else:
            await interaction.response.send_message("Nie masz permisji", ephemeral=True)
    
    '''@tasks.loop(hours=24, count=2)
    async def info_share(self, info, message, channel):
        if polls.info_share.current_loop >= 2:
            member:discord.User = info.author
            await channel.send(f"{member.mention} {info}", reference=message)'''


    @command()
    async def find_poll(ctx, self, message_id:int):
        if self.author.id != 742425630024400897:
            pass
        for polls_instance in ctx.bot.polls_instances_list:
            message = polls_instance[1]
            instance = polls_instance[0]
            turn = polls_instance[2]
            nonvoters_list = [member.mention for member in await polls.find_nonvoters(self, instance)]
            nonvoters_str =", ".join(nonvoters_list)
            if int(message.id) == message_id:
                await self.send(content = f"**Tytuł**: {instance.title} \n"
                            + f"**Autor**: {instance.author}\n"
                            + f"**Kolejka**: {turn} z 8\n"
                            + f"**Zagłosowali**: {[member.name for member in instance.overall_list]} \n"
                            + f"**Widoczność**: {instance.admin_text} \n"
                            + f"**Brak głosu**: {nonvoters_str}")
                

    
    async def find_nonvoters(self, poll_instance) -> list:
        available_to_vote = poll_instance.channel.members[:50]
        users_converted_to_members = [poll_instance.channel.guild.get_member(ThreadMember.id) for ThreadMember in available_to_vote]
        nonvoters = [member.mention for member in users_converted_to_members if (member not in poll_instance.overall_list and not member.bot)]
        return nonvoters


    @tasks.loop(time=reminder_hours)
    async def nonvoters_reminder(ctx, self):
        temp_instances_list = []
        for polls_instance in self.bot.polls_instances_list:
            message = polls_instance[1]
            instance = polls_instance[0]
            turn = polls_instance[2]
            if (turn <= 8 and message.guild.id == 1198978337150881812) or message.guild.id == 963476559585505360:
                temp_instances_list.append(polls_instance)
        self.bot.polls_instances_list.clear()
        for polls_instance in temp_instances_list:
            nonvoters_list = [member.mention for member in await polls.find_nonvoters(self, instance)]
            if len(nonvoters_list) < 1:
                continue
            nonvoters_str =", ".join(nonvoters_list)
            await instance.channel.send(nonvoters_str + "\nHej, nie zagłosowaliście jeszcze w głosowaniu wyżej. Zróbcie to proszę! Link do głosowania: " + message.jump_url)
            polls_instance[2] += 1    
        self.bot.polls_instances_list = temp_instances_list

    
    @command()
    async def reminder_start(ctx, self):
        if self.author.id == 742425630024400897:
            polls.nonvoters_reminder.start(ctx, self)
            print("Reminder ankiet: ON")
    
    @command()
    async def reminder_stop(ctx, self):
        if self.author.id == 742425630024400897:
            polls.nonvoters_reminder.cancel()
            print("Reminder ankiet: OFF")


    @command()
    async def polls_instances_list(ctx, self):
        if self.author.id != 742425630024400897: 
            pass
        for item in self.bot.polls_instances_list:
            if len(item) != 3:
                instance = item[0]
                message = item[1]
                print(f"Title: {instance.title}, Author: {instance.author}, Data: {message.created_at}")
            instance = item[0]
            message = item[1]
            turn = item[2]
            print(f"Title: {instance.title}, Author: {instance.author}, Data: {message.created_at}, Kolejka: {turn}")


    @command()
    async def clear_ins(ctx, self):
        self.bot.polls_instances_list.clear()

    disabled_reminders = []
    @command()
    async def disable_reminder(ctx, self, poll_id:int): #poll_id = message.id
        if self.guild.id != 1198978337150881812:
            pass
        polls.disabled_reminders.append(poll_id)



async def setup(bot: Bot):
    await bot.add_cog(polls(bot))





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
from dataclasses import dataclass



con = sqlite3.connect('data/selfies_database.db')
con.row_factory = sqlite3.Row
cur = con.cursor()



class counter_ex(Cog):

    intents = discord.Intents.all()
    intents.message_content = True
    intents.members = True
    intents.guilds = True
    
    def __init__(self, bot: Bot):
        self.bot = bot
        
    

    
    '''@command()
    async def count(ctx, self, month:int):
        if self.author.id == 742425630024400897:
            raport_channel = self.bot.get_channel(1188542888989163620)
            date = str(t.strftime("%Y-%m-%d"))
            CWD = Path(os.getcwd())
            FileName = Path(f"Raport_Selfies_{date}.txt")
            FilePath = PurePath(CWD, FileName)
            nicks = await counter_ex.selfies(ctx, self, month)
            with open(f"Raport_Selfies_{date}.txt", "a+") as f:
                for users_list in nicks:
                    for i in users_list.items():
                        print(f"Nick: {i[0]}, Selfies: {i[1][0]}, Vids: {i[1][1]}", file=f)
            await raport_channel.send(file = discord.File(FilePath))
            os.remove(FilePath)
            
            date = str(t.strftime("%Y-%m-%d"))          
            CWD = Path(os.getcwd())
            FileName = Path(f"Raport_Galeria_{date}.txt")
            FilePath = PurePath(CWD, FileName)            
            gal_names = await counter_ex.gallery(ctx, self, month)
            with open(f"Raport_Galeria_{date}.txt", "a+") as f:
                for x in gal_names.items():
                    print(f"Nick: {x[0]}, Num: {x[1]}", file=f)
            await raport_channel.send(file = discord.File(FilePath))
            os.remove(FilePath)'''

                

    '''async def gallery(ctx, self, month):
        ending_month = 1 if month == 12 else month +1
        selfies_channel = self.bot.get_channel(412146947412197396)
        gal_names = {}
        async for msg in selfies_channel.history(
            limit=2000,
            after=datetime.datetime(2024, month, 1),
            before=datetime.datetime(2024, ending_month, 1),
        ):
            try:  # sprawdza selfies powyżej 25 like
                like_emoji = discord.utils.get(
                    self.bot.emojis, name="like"
                )  # na przestrzeni ostatnich 45 dni
                reaction = discord.utils.get(
                    msg.reactions, emoji=like_emoji
                )  # za wyjątkiem ostatnich 15 dni
                if reaction.count >= 25:
                    if msg.author.id not in gal_names:
                        gal_names[msg.author.id] = [0,0,1,0,0]
                    elif msg.author.id in gal_names:
                        gal_names[msg.author.id][2] += 1
            except AttributeError:
                pass
        f = open("output.txt", "a")
        list = [i for i in gal_names.items()]
        await counter_ex.command_maker(self, list, " Punkty za galerię")
        return gal_names      '''
        
    
    @dataclass
    class schannel:
        id:discord.TextChannel
        nicks: dict
        vids:list
        group_photos:list
        has_no_role:list
        doubles:list
        triples:list



    @command()
    async def selfies(ctx, self, start_date, end_date):
        if not self.author.id == 762068995028549684:
            return
        start_date = [int(i) for i in start_date.split("-")]
        end_date = [int(i) for i in end_date.split("-")]
        #day, month, year: 30-12-2024
        OK_user_object = ctx.bot.get_user(762068995028549684)
        atencjusz_role = discord.utils.get(self.guild.roles, name="Atencjusz")
        #channelprop, nicks, vids, group_photos, has_no_role
        channels = {
            "selfies_channel" : counter_ex.schannel(ctx.bot.get_channel(1199385908517032026), {}, [], [], [], [], []), #type:ignore
            "selfies_plus_channel" : counter_ex.schannel(ctx.bot.get_channel(412146947412197396), {}, [], [], [], [], []) #type:ignore
            }
        list_one=[]
        list_two=[]

        for channel_name in channels:
            channel = channels[channel_name]
            async for msg in channel.id.history(
                limit = 5000,
                after=datetime.datetime(start_date[2], start_date[1], start_date[0]),
                before=datetime.datetime(end_date[2], end_date[1], end_date[0]),
            ):
                member = self.guild.get_member(msg.author.id)
                if member:
                    forced_break = False
                    for reaction in msg.reactions:
                        if reaction.emoji == "❌":
                            users = [user async for user in reaction.users()]
                            for single_user in users:
                                if single_user.id == 762068995028549684:
                                    forced_break = True
                        elif reaction.emoji == "🎬":
                            users = [user async for user in reaction.users()]
                            for muser in users:
                                if muser.id == 762068995028549684:
                                    channel.vids.append(msg.author.id)
                        elif reaction.emoji == "🎀":
                            users = [user async for user in reaction.users()]
                            for muser in users:
                                if muser.id == 762068995028549684:  
                                    channel.group_photos.append(msg.jump_url)
                                    forced_break = True
                        elif reaction.emoji == "2️⃣":
                            users = [user async for user in reaction.users()]
                            for muser in users:
                                if muser.id == 762068995028549684:
                                    channel.doubles.append(msg.author.id)

                        elif reaction.emoji == "3️⃣":
                            users = [user async for user in reaction.users()]
                            for muser in users: 
                                if muser.id == 762068995028549684:
                                    channel.triples.append(msg.author.id)

                    
                    if forced_break == True:
                        continue
                    if msg.author.id not in channel.nicks:
                        channel.nicks[msg.author.id] = [1, 0, 0, 0, 0]
                        #[selfies, vids, galleries, doubles, triples]
                    elif msg.author.id in channel.nicks:
                        channel.nicks[msg.author.id][0] += 1
                    try:
                        if atencjusz_role not in msg.author.roles:  #type:ignore
                            channel.has_no_role.append(msg.author.id)
                    except AttributeError:
                        continue    
            for user_id, k in channel.nicks.items():    
                user_id = int(user_id)
                #[selfies, vids, galleries, doubles, triples]           
                channel.nicks[user_id][1] = int(channel.vids.count(user_id))
                channel.nicks[user_id][0] -= channel.nicks[user_id][1]
                channel.nicks[user_id][3] = int(channel.doubles.count(user_id))
                channel.nicks[user_id][4] = int(channel.triples.count(user_id))
                channel.nicks[user_id][0] -= channel.nicks[user_id][3]
                channel.nicks[user_id][0] -= channel.nicks[user_id][4]
            lista = [i for i in channel.nicks.items()]
            await counter_ex.command_maker(ctx, lista, f"{channel_name}")
            for url in channel.group_photos:
                await OK_user_object.send("Zdjęcie grupowe: "+url) #type:ignore
            for i in list(set(channel.has_no_role)):
                try:
                    member = discord.utils.get(self.guild.members, id = i)
                    await OK_user_object.send("Brak rangi Atencjusz:"+member.mention) #type:ignore
                except AttributeError:
                    continue
            if channel_name == "selfies_channel":
                list_one = channel.nicks
            else:
                list_two = channel.nicks
        return [list_one, list_two]      
    
    
    async def command_maker(self, id, reason:str):
        OK_user_object = self.bot.get_user(762068995028549684)
        points = {}
        
        selfie_value = 75 if reason == "selfies_plus_channel" else 50
        vid_value = 100 if reason == "selfies_plus_channel" else 75
        gal_value = 200
        double_value = 150 if reason == "selfies_plus_channel" else 100
        triple_value = 225 if reason == "selfies_plus_channel" else 150
        
        for i in id:
            pointquan = int(i[1][0] * selfie_value + i[1][1] * vid_value + i[1][2]*gal_value + i[1][3]*double_value + i[1][4]*triple_value)
            points[i[0]] = pointquan
        new_dict = { }
        for keys in points:
            new_dict[points[keys]] = [ ]
        for keys in points:
            new_dict[points[keys]].append(keys)
        for key, value in new_dict.items():
            command_string = f".punkty-dodaj {key}"
            for i in value:
                command_string = command_string + f" <@{i}>"
            await OK_user_object.send(content = "`"+command_string+"`" + " " +reason) #type:ignore
            await asyncio.sleep(2)

	
		
	
    @command()
    async def selfies_dbg(ctx, self, start_date, end_date):
        if not self.author.id == 742425630024400897:
            return
        start_date = [int(i) for i in start_date.split("-")]
        end_date = [int(i) for i in end_date.split("-")]
        #day, month, year: 30-12-2024
        OK_user_object = ctx.bot.get_user(742425630024400897)
        atencjusz_role = discord.utils.get(self.guild.roles, name="Atencjusz")
        #channelprop, nicks, vids, group_photos, has_no_role
        channels = {
            "selfies_channel" : counter_ex.schannel(ctx.bot.get_channel(1199385908517032026), {}, [], [], [], [], []), #type:ignore
            "selfies_plus_channel" : counter_ex.schannel(ctx.bot.get_channel(412146947412197396), {}, [], [], [], [], []) #type:ignore
            }
        list_one=[]
        list_two=[]

        for channel_name in channels:
            channel = channels[channel_name]
            async for msg in channel.id.history(
                limit = 5000,
                after=datetime.datetime(start_date[2], start_date[1], start_date[0]),
                before=datetime.datetime(end_date[2], end_date[1], end_date[0]),
            ):
                member = self.guild.get_member(msg.author.id)
                if member:
                    forced_break = False
                    for reaction in msg.reactions:
                        if reaction.emoji == "❌":
                            users = [user async for user in reaction.users()]
                            for single_user in users:
                                if single_user.id == 762068995028549684:
                                    forced_break = True
                        elif reaction.emoji == "🎬":
                            users = [user async for user in reaction.users()]
                            for muser in users:
                                if muser.id == 762068995028549684:
                                    channel.vids.append(msg.author.id)
                        elif reaction.emoji == "🎀":
                            users = [user async for user in reaction.users()]
                            for muser in users:
                                if muser.id == 762068995028549684:  
                                    channel.group_photos.append(msg.jump_url)
                                    forced_break = True
                        elif reaction.emoji == "2️⃣":
                            users = [user async for user in reaction.users()]
                            for muser in users:
                                if muser.id == 762068995028549684:
                                    channel.doubles.append(msg.author.id)

                        elif reaction.emoji == "3️⃣":
                            users = [user async for user in reaction.users()]
                            for muser in users: 
                                if muser.id == 762068995028549684:
                                    channel.triples.append(msg.author.id)

                    
                    if forced_break == True:
                        continue
                    if msg.author.id not in channel.nicks:
                        channel.nicks[msg.author.id] = [1, 0, 0, 0, 0]
                        #[selfies, vids, galleries, doubles, triples]
                    elif msg.author.id in channel.nicks:
                        channel.nicks[msg.author.id][0] += 1
                    try:
                        if atencjusz_role not in msg.author.roles:  #type:ignore
                            channel.has_no_role.append(msg.author.id)
                    except AttributeError:
                        continue    
            for user_id, k in channel.nicks.items():    
                user_id = int(user_id)
                #[selfies, vids, galleries, doubles, triples]           
                channel.nicks[user_id][1] = int(channel.vids.count(user_id))
                channel.nicks[user_id][0] -= channel.nicks[user_id][1]
                channel.nicks[user_id][3] = int(channel.doubles.count(user_id))
                channel.nicks[user_id][4] = int(channel.triples.count(user_id))
                channel.nicks[user_id][0] -= channel.nicks[user_id][3]
                channel.nicks[user_id][0] -= channel.nicks[user_id][4]
            lista = [i for i in channel.nicks.items()]
            await counter_ex.command_maker_dbg(ctx, lista, f"{channel_name}")
            for url in channel.group_photos:
                await OK_user_object.send("Zdjęcie grupowe: "+url) #type:ignore
            for i in list(set(channel.has_no_role)):
                try:
                    member = discord.utils.get(self.guild.members, id = i)
                    await OK_user_object.send("Brak rangi Atencjusz:"+member.mention) #type:ignore
                except AttributeError:
                    continue
            if channel_name == "selfies_channel":
                list_one = channel.nicks
            else:
                list_two = channel.nicks
        return [list_one, list_two]      
    
    
    async def command_maker_dbg(self, id, reason:str):
        OK_user_object = self.bot.get_user(742425630024400897)
        points = {}
        
        selfie_value = 75 if reason == "selfies_plus_channel" else 50
        vid_value = 100 if reason == "selfies_plus_channel" else 75
        gal_value = 200
        double_value = 150 if reason == "selfies_plus_channel" else 100
        triple_value = 225 if reason == "selfies_plus_channel" else 150
        
        for i in id:
            pointquan = int(i[1][0] * selfie_value + i[1][1] * vid_value + i[1][2]*gal_value + i[1][3]*double_value + i[1][4]*triple_value)
            points[i[0]] = pointquan
        new_dict = { }
        for keys in points:
            new_dict[points[keys]] = [ ]
        for keys in points:
            new_dict[points[keys]].append(keys)
        for key, value in new_dict.items():
            command_string = f".punkty-dodaj {key}"
            for i in value:
                command_string = command_string + f" <@{i}>"
            await OK_user_object.send(content = "`"+command_string+"`" + " " +reason) #type:ignore
            await asyncio.sleep(2)
    
    '''@app_commands.command(name="daily", description="Komenda dla Opiekunów Kanału do automatycznego zliczania daily - tworzy gotową komendę z punktami.")
    @app_commands.describe(points="Ilość punktów do rozdania. Wpisz proszę kolejne poziomy oddzielone slashem, np. '50/75/100/125/150'", 
                           date="Data daily (format DD-MM-RRRR). W przypadku braku konkretnej daty, automatycznie wybierze dzisiejszą.", 
                           channel="ID kanału do policzenia daily. Jeśli nie podasz konkretnego kanału, wybierze ten, na którym wpisujesz komendę.",
                           #days_and_count="Maksymalna ilość dni daily streaka"
                           )
    async def schedule(self, interaction: discord.Interaction, days:int, points:str, date:str=None, channel:discord.TextChannel=None):
        OK_role = interaction.guild.get_role(412193755286732800)
        if OK_role in interaction.user.roles:    
            if not channel:
                channel = interaction.channel
            if not date:
                date = f"{datetime.datetime.today().day}-{datetime.datetime.today().month}-{datetime.datetime.today().year}"
            date_list = date.split("-")
            date_int_list = [int(i) for i in date_list]
            starting_date = datetime.datetime(year=date_int_list[2], month=date_int_list[1], day=date_int_list[0])

            users_with_daily = {} #{member: his daily message}
            daily_streak = {}  #{member: streak_int)
            dates = [starting_date - datetime.timedelta(days=n) for n in range(0, days)]
            
            is_looping = True
            forced_break = False
            await interaction.response.send_message("Liczę...", ephemeral=True)
            for day in dates:
                async for message in channel.history(before=day+datetime.timedelta(days=1), after=day-datetime.timedelta(seconds=1), limit=20000):
                    if "#daily" in message.content:
                        if (message.author.id not in users_with_daily) and (abs((dates[0].day - message.created_at.replace(tzinfo=None).day)) <= 2):
                            users_with_daily[message.author.id] = message.created_at.replace(tzinfo=None)
                            daily_streak[message.author.id] = 1
                        elif message.author.id in users_with_daily:
                            if abs((day.day - users_with_daily[message.author.id].day)) == 1 or abs((day.day - users_with_daily[message.author.id].day)) == 0:
                                daily_streak[message.author.id] += 1
                                users_with_daily[message.author.id] = message.created_at.replace(tzinfo=None)
                    else:
                        if users_with_daily:
                            if abs(message.created_at.replace(tzinfo=None).day - users_with_daily[max(daily_streak, key=daily_streak.get)].day) >= 3:
                                is_looping = False
                                break
                if is_looping == False:
                    break
            await counter_ex.daily_command_maker(self, interaction.channel, points, daily_streak)


    async def daily_command_maker(self, channel, points:str, daily_streak:list):
        points = points.split("/")
        points_list = [int(num) for num in points]
        points_dict={}
        for member, stk_value in daily_streak.items():
            points_dict[member] = points_list[stk_value-1] if stk_value <= len(points_list) else points_list[len(points_list)-1]
        inverted_dict = {}
        for keys in points_dict:
            inverted_dict[points_dict[keys]] = [ ]
        for keys in points_dict:
            inverted_dict[points_dict[keys]].append(keys)
        whole_command_string = ""
        for key, value in inverted_dict.items():
            command_string = f".punkty-dodaj {key}"
            for i in value:
                command_string = command_string + f" <@{i}>"
            whole_command_string += f"`{command_string}`\n"       
        await channel.send(content = f"{whole_command_string}")'''
                        
					
            
    '''@command()
    async def daily_test1(self, interaction: discord.Interaction, points:str, date:str=None, channel:int=None):
        if not channel:
            channel = interaction.channel
        elif channel:
            channel = self.bot.get_channel(channel)
        if not date:
            date = f"{datetime.datetime.today().day}-{datetime.datetime.today().month}-{datetime.datetime.today().year}"
        date_list = date.split("-")
        date_int_list = [int(i) for i in date_list]
        starting_date = datetime.datetime(year=date_int_list[2], month=date_int_list[1], day=date_int_list[0])

        users_with_daily = {} #{member: his daily message}
        daily_streak = {}  #{member: streak_int)
        dates = [starting_date - datetime.timedelta(days=n) for n in range(0, 7)]
        print(dates)
        for day in dates:
            async for message in channel.history(around=day):
                if "#daily" in message.content:
                    if message.author.id not in users_with_daily:
                        print("dupa")
                        users_with_daily[message.author.id] = message.created_at.replace(tzinfo=None)
                        daily_streak[message.author.id] = 1
                    else:
                        print(abs((day - users_with_daily[message.author.id]).days))
                        print(message.author.name)
                        if abs((day - users_with_daily[message.author.id]).days) == 1 or abs((day - users_with_daily[message.author.id]).days) == 0:
                            daily_streak[message.author.id] += 1
                            users_with_daily[message.author.id] = message.created_at.replace(tzinfo=None)
                        elif abs((day - users_with_daily[message.author.id]).days) >= 2:
                            daily_streak[message.author.id] = 1
        await counter_ex.daily_command_maker(self, interaction.channel, points, daily_streak)'''


    '''@command()
    async def agumo_count(self, ctx, month:int, day:int):
        if ctx.author.id == 742425630024400897 or ctx.author.id == 206488012786237440:
            klik_channel = ctx.bot.get_channel(1076081025114964008)
            prev_member = None
            members_list = {}
            async for message in klik_channel.history(limit=5000, after=datetime.datetime(2024, month, day)):
                if "klik" in message.content[0:4].lower() and prev_member != message.author.id:
                    try:
                        members_list[message.author.name] += 1
                    except KeyError:
                        members_list[message.author.name] = 1
                    prev_member = message.author.id
            list_string = ""
            for key, item in members_list.items():
                list_string = list_string + f"`{key}`: {item} klików\n"
            
            await ctx.author.send(list_string) '''

    
    @Cog.listener("on_message")
    async def przywitaj_się_thread_maker(self, message):
        welcome_channel = self.bot.get_channel(412202170549796874)
        if message.channel.id == welcome_channel.id and not message.author.bot: #type:ignore
            await message.create_thread(name="Witamy w naszych progach!!! ♡", auto_archive_duration=1440)




async def setup(bot: Bot):
    await bot.add_cog(counter_ex(bot))

    '''@command()
    async def selfies_test(ctx, self, start_date, end_date) -> list:     
        start_date = start_date.split("-")
        end_date = end_date.split("-")
        #day, month, year: 30-12-2024
        raport_channel = ctx.bot.get_channel(1188542888989163620)
        atencjusz_role = discord.utils.get(self.guild.roles, name="Atencjusz")
        
        #channelprop, nicks, vids, group_photos, has_no_role
        selfies_channel = channel(0, {}, [], [], [], [], [])
        selfies_plus_channel = channel(0, {}, [], [], [], [], [])
        channels = [selfies_channel, selfies_plus_channel]
        list_one=[]
        list_two=[]

        for channel in channels:
            channel_property = self.bot.get_channel(channel.id)
            async for msg in channel_property.history(
                limit = 1000,
                after=datetime.datetime(start_date[2], start_date[1], start_date[0]),
                before=datetime.datetime(end_date[2], end_date[1], end_date[0]),
            ):
                member = self.guild.get_member(msg.author.id)
                if not member:
                    continue
                forced_break = False
                for reaction in msg.reactions:
                    if reaction.emoji == "❌":
                        users = [user async for user in reaction.users()]
                        for single_user in users:
                            if single_user.id == 742425630024400897:
                                forced_break = True
                    elif reaction.emoji == "🎬":
                        users = [user async for user in reaction.users()]
                        for muser in users:
                            if muser.id == 742425630024400897:
                                channel.vids.append(msg.author.name)
                    elif reaction.emoji == "🎀":
                        users = [user async for user in reaction.users()]
                        for muser in users:
                            if muser.id == 742425630024400897:  
                                channel.group_photos.append(msg.jump_url)
                                forced_break = True
                    elif reaction.emoji == "2️⃣":
                        users = [user async for user in reaction.users()]
                        for muser in users:
                            if muser.id == 742425630024400897:
                                channel.doubles.append(msg.author.name)
                                forced_break = True
                    elif reaction.emoji == "3️⃣":
                        users = [user async for user in reaction.users()]
                        for muser in users: 
                            if muser.id == 742425630024400897:
                                channel.triples.append(msg.author.name)
                                forced_break=True



                
                if forced_break == True:
                    continue
                if msg.author.id not in channel.nicks:
                    channel.nicks[msg.author.id] = [1, 0, 0, 0, 0]
                elif msg.author.id in channel.nicks:
                    channel.nicks[msg.author.id][0] += 1
                try:
                    if atencjusz_role not in msg.author.roles:
                        channel.has_no_role.append(msg.author.id)
                except AttributeError:
                    continue    
            
            for n in channel.nicks.items():
                channel.nicks[n[0]][1] = int(channel.vids.count(str(n[0])))
                channel.nicks[n[0]][0] -= channel.nicks[n[0]][1]
                channel.nicks[n[0]][3] = int(channel.doubles.count(str(n[0])))
                channel.nicks[n[0]][4] = int(channel.triples.count(str(n[0])))
            lista = [i for i in channel.nicks.items()]
            await counter_ex.command_maker(self, lista, f" {channel}")
            for url in channel.group_photos:
                await raport_channel.send("Zdjęcie grupowe: "+url)
            for i in list(set(channels[channel][4])):
                try:
                    member = discord.utils.get(self.guild.members, id = i)
                    await raport_channel.send("Brak rangi Atencjusz:"+member.mention)
                except AttributeError:
                    continue
            if channel == "selfies_channel":
                list_one = channel.nicks
            else:
                list_two = channels[channel][1]
        return [list_one, list_two] '''



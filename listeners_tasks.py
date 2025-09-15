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
from dataclasses import dataclass


con = sqlite3.connect('data/selfies_database.db')
con.row_factory = sqlite3.Row
cur = con.cursor()


time = datetime.time(hour=0, minute=5, tzinfo=ZoneInfo("Europe/Warsaw"))
gallery_times = [
    datetime.time(hour=1,minute=7,tzinfo=ZoneInfo("Europe/Warsaw")),
    datetime.time(hour=8,tzinfo=ZoneInfo("Europe/Warsaw")),
    datetime.time(hour=15, minute=6,tzinfo=ZoneInfo("Europe/Warsaw")),
    datetime.time(hour=18, minute=31,tzinfo=ZoneInfo("Europe/Warsaw")),
    datetime.time(hour=19, minute=7,tzinfo=ZoneInfo("Europe/Warsaw"))
]

birthday_time = datetime.time(hour=12)
                



class listeners_tasks(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        
    @Cog.listener()
    async def on_ready(self):
        self.selfies_channel = self.bot.get_channel(412146947412197396)
        self.selfies_bot_channel = self.bot.get_channel(1179884652522115102)
        self.raport_channel = self.bot.get_channel(1188542888989163620)
        self.id_channel = self.bot.get_channel(1201517637197365319)
        self.gallery_channel = self.bot.get_channel(497361494833496064)
        
    @command()
    async def birthday_manual_trigger(self, ctx):
        await listeners_tasks.birthday_checker(self, ctx)
    
    @tasks.loop(time=birthday_time)
    async def birthday_checker(ctx, self):
        birthday_role = discord.utils.get(self.guild.roles, id = 1250518611114721312)
        urodziny_channel = ctx.bot.get_channel(628530693386797076)
        td_month = (t.strftime("%m"))
        td_day = (t.strftime("%d"))
        date = td_month+"-"+td_day
        print(date)
        cur.execute("SELECT user_id FROM birthdays WHERE date = ?", (date,))
        wynik = cur.fetchall()
        if wynik is None: 
            pass
        else:
            for user in wynik:
                if user is not None:
                    CWD = Path(os.getcwd())
                    member = ctx.bot.get_user(user[0])
                    if member is None:
                        continue
                    else:
                        path_to_avatar = str(PurePath(CWD, Path(f"avatar{member.name}.png")))
                        path_to_main_image = str(PurePath(CWD, Path("main_img.png")))
                        await member.avatar.save(fp=path_to_avatar)
                        main_img = Image.open(fp=path_to_main_image).convert("RGBA")
                        avatar = Image.open(fp=path_to_avatar).convert("RGBA")
                        resized_avatar = avatar.resize((500, 500))
                        background = Image.new("RGBA", resized_avatar.size, (0,0,0,0))
                        mask = Image.new("RGBA", resized_avatar.size, 0)
                        draw = ImageDraw.Draw(mask)
                        draw.ellipse((0,0,500,500), fill='green', outline=None)
                        transc_avatar = Image.composite(resized_avatar, background, mask)
                        avatar_img = Image.new("RGBA", main_img.size, (255, 255, 255, 0))
                        avatar_img.paste(transc_avatar, (1356,70))
                    
                        out = Image.alpha_composite(main_img, avatar_img)

                        birthday_role = discord.utils.get(self.guild.roles, id = 1250518611114721312)
                        texts = [f"## 🎉 Hej {birthday_role.mention}! Dzisiaj mamy szczególny dzień - to urodziny {member.mention}!",
                                 f"## 🎂 {birthday_role.mention}, nie zapomnijcie o {member.mention}! Dziś obchodzi swoje urodziny!",
                                 f"## 🎁 Hej, {birthday_role.mention}! {member.mention} ma dziś urodziny! Ślijcie życzenia!",
                                 f"## 🌟 Uwaga, uwaga {birthday_role.mention}! Dziś świętujemy urodziny {member.mention}!"]

                        with BytesIO() as file:
                            out.save(file, format="PNG")
                            file.seek(0)
                            discord_file = discord.File(file, filename="image.png")
                            await urodziny_channel.send(content = texts[random.randint(0, 3)], file=discord_file)
                        cur.execute("UPDATE birthdays SET done=? WHERE user_id = ?", (1, user[0],))
                        con.commit()
                        os.remove(path_to_avatar)

    @command()
    async def b_man(ctx, self):
        CWD = Path(os.getcwd())
        urodziny_channel = ctx.bot.get_channel(628530693386797076)
        pluszak = ctx.bot.get_user(215838737102405632)
        siup = ctx.bot.get_user(158168045506789376)
        users = [pluszak, siup]
        for member in users:
            path_to_avatar = str(PurePath(CWD, Path(f"avatar{member.name}.png")))
            path_to_main_image = str(PurePath(CWD, Path("main_img.png")))
            await member.avatar.save(fp=path_to_avatar)
            main_img = Image.open(fp=path_to_main_image).convert("RGBA")
            avatar = Image.open(fp=path_to_avatar).convert("RGBA")
            resized_avatar = avatar.resize((500, 500))
            background = Image.new("RGBA", resized_avatar.size, (0,0,0,0))
            mask = Image.new("RGBA", resized_avatar.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0,0,500,500), fill='green', outline=None)
            transc_avatar = Image.composite(resized_avatar, background, mask)
            avatar_img = Image.new("RGBA", main_img.size, (255, 255, 255, 0))
            avatar_img.paste(transc_avatar, (1356,70))
        
            out = Image.alpha_composite(main_img, avatar_img)

            birthday_role = discord.utils.get(self.guild.roles, id = 1250518611114721312)
            texts = [f"## 🎉 Hej {birthday_role.mention}! Wczoraj mieliśmy szczególny dzień - urodziny {member.mention}!",
                        f"## 🎂 {birthday_role.mention}, nie zapomnijcie o {member.mention}! Wczoraj miałx swoje urodziny!",
                        f"## 🎁 Hej, {birthday_role.mention}! {member.mention} miałx wczoraj urodziny! Ślijcie życzenia!",
                        f"## 🌟 Uwaga, uwaga {birthday_role.mention}! Wczoraj świętowaliśmy urodziny {member.mention}!"]

            with BytesIO() as file:
                out.save(file, format="PNG")
                file.seek(0)
                discord_file = discord.File(file, filename="image.png")
                await urodziny_channel.send(content = texts[random.randint(0, 3)], file=discord_file)

    
    @tasks.loop(time=time)
    async def db_copy(ctx, self):
        raport_channel = self.bot.get_channel(1188542888989163620)
        CWD = Path(os.getcwd())
        date = t.strftime("%Y_%m_%d")
        path = PurePath(CWD, Path("data/selfies_database.db"))
        if int(t.strftime("%d"))%2 != 0:
            os.system(f'cp {path} selfies_database_copy_{date}.db')
            copy_path = PurePath(CWD, Path(f"selfies_database_copy_{date}.db"))
            await raport_channel.send(file = discord.File(copy_path))
            os.remove(copy_path)


    @tasks.loop(time=time)
    async def months_changer(ctx, self):
        raport_channel = self.bot.get_channel(1188542888989163620)
        date = t.strftime("%Y-%m-%d %H:%M")
        if int(t.strftime("%d")) == 1:
            cur.execute("UPDATE `months` SET month0=month1")
            cur.execute("UPDATE `months` SET month1=month2")
            cur.execute("UPDATE `months` SET month2=month3")
            cur.execute("UPDATE `months` SET month3=month4")
            cur.execute("UPDATE `months` SET month4=month5")
            cur.execute("UPDATE `months` SET month5=0")
            cur.execute("UPDATE `months` SET gallery0=gallery1")
            cur.execute("UPDATE `months` SET gallery1=gallery2")
            cur.execute("UPDATE `months` SET gallery2=gallery3")
            cur.execute("UPDATE `months` SET gallery3=gallery4")
            cur.execute("UPDATE `months` SET gallery4=gallery5")
            cur.execute("UPDATE `months` SET gallery5=0")
            con.commit()
            await raport_channel.send(
                f"{date} | Tabele `months` uaktualnione na nowy miesiąc"
            )
            listeners_tasks.months_changer.restart(ctx, self)
        elif int(t.strftime("%d")) != 1:
            await raport_channel.send(
                f"{date} | Pętla months_changer wykonała się bez zmiany kolejności kolumn"
            )
            listeners_tasks.months_changer.restart(ctx, self)

    @command()
    async def loop_start(ctx, self):
        if self.author.id == 742425630024400897:
            listeners_tasks.months_changer.start(ctx, self)
            listeners_tasks.gallery_checker.start(ctx, self)
            listeners_tasks.db_copy.start(ctx, self)
            listeners_tasks.birthday_checker.start(ctx, self)
            print("done")
        else:
            self.send("Nie masz permisji nubku")
            
    @command()
    async def loop_stop(ctx, self):
        if self.author.id == 742425630024400897:
            listeners_tasks.months_changer.cancel()
            listeners_tasks.gallery_checker.cancel()
            listeners_tasks.db_copy.cancel()
            listeners_tasks.birthday_checker.cancel()
            print("done")
        else:
            self.send("Nie masz permisji nubku")     
    
    
    @dataclass
    class category:
        ids_channel_id:int
        gallery_channel_id:int
        photos_channel_id:int
        prog:int
        name:str
        
    @command()
    async def manual_gallery_trigger(ctx, self, days_count=None):
       await listeners_tasks.gallery_checker(ctx, self, days_count)
        
    @tasks.loop(time=gallery_times)
    async def gallery_checkertest(ctx, self, days_count=None):
        days_count = int(days_count) if days_count else 15
        
        categories = [
            listeners_tasks.category(1201517637197365319, 497361494833496064, 412146947412197396, 25, "Galeria Strefy Selfies"),
            listeners_tasks.category(130050655631573001, 1297947980573179934, 532659818071064586, 15, "Galeria Strefy Niesfornej"),
            listeners_tasks.category(1211334897713553539, 879843101626224741, 412147997489627146, 7, "Galeria Strefy Kuchni"),
            listeners_tasks.category(1211334865954545694, 856870066175868968, 412147918980644864, PLACEHOLDER, "Galeria Strefy Pupili")
        ]
        
        tday = (datetime.date.today() - datetime.timedelta(days=days_count)).day
        tmonth = (datetime.date.today() - datetime.timedelta(days=days_count)).month
        tyear = (datetime.date.today() - datetime.timedelta(days=days_count)).year
        
        photos_channel_property = ctx.bot.get_channel(category.photos_channel_id)
        gallery_channel_property = ctx.bot.get_channel(category.gallery_channel_id)
        ids_channel_property = ctx.bot.get_channel(category.ids_channel_id)
        
        CWD = Path(os.getcwd())
        counters = Path("grafiki/liczniki")
        for category in categories:
            if category.name == "Galeria Strefy Kuchni":
                continue
            async for msg in photos_channel_property.history(after=datetime.datetime(tyear, tmonth, tday)):
                form = 0
                if category.name == "Galeria Strefy Pupili":
                    like_emoji = discord.utils.get(ctx.bot.emojis, name="serducho")
                else:
                    like_emoji = discord.utils.get(ctx.bot.emojis, name="like")
                reaction = discord.utils.get(msg.reactions, emoji=like_emoji)
                try:
                    if reaction.count >= category.prog:
                        cur.execute("SELECT current_counter FROM players WHERE id = ?", (msg.author.id,))
                        counter = cur.fetchone()[0]
                        if counter == None:
                            counter = "count_basic.png"
                        path_to_counter = str(PurePath(CWD, counters, Path(counter)))
                        attachment = msg.attachments[0]
                        e=discord.Embed(title=f"{msg.jump_url}", description=category.name,color=discord.Color.yellow())
                        e.set_image(url=attachment.url)
                        base = Image.open(fp = path_to_counter).convert("RGBA")
                        max_width =base.size[0]
                        max_height =base.size[1]
                        txt = Image.new("RGBA", (max_width, max_height), (255,255,255,0))
                        draw = ImageDraw.Draw(txt)
                        fnt = ImageFont.truetype("AGENCYR.TTF", 290)
                        size = draw.textbbox(xy = (0,0),text=f"{reaction.count}", font=fnt)
                        wszerz = size[2]
                        draw.text(xy=((max_width-wszerz)/2,45), text=f"{reaction.count}", font=fnt, fill=(255,255,255,255))
                        out = Image.alpha_composite(base, txt)
                        e.set_author(name = f"{msg.author.name}", icon_url = msg.author.avatar.url)
                        async for message in ids_channel_property.history(after=datetime.datetime(tyear, tmonth, tday)):
                            id_list = list(message.content.split(","))
                            if msg.id != int(id_list[0]):
                                continue
                            elif msg.id == int(id_list[0]):
                                form = 1 
                                gallery_message = await gallery_channel_property.fetch_message(int(id_list[1]))
                                with BytesIO() as file:
                                    out.save(file, format="PNG")
                                    file.seek(0)
                                    discord_file = discord.File(file, filename="image.png")
                                    e.set_thumbnail(url = "attachment://image.png")
                                    await gallery_message.edit(embed=e, attachments=[discord_file])
                        if form == 0:
                            with BytesIO() as file:
                                out.save(file, format="PNG")
                                file.seek(0)
                                discord_file = discord.File(file, filename="image.png")
                                e.set_thumbnail(url = "attachment://image.png")
                                gallery_message = await gallery_channel_property.send(embed=e, file=(discord_file))
                                if category.name == "Galeria Strefy Selfies":
                                    cur.execute("SELECT gallery FROM players WHERE id = ?", (msg.author.id,)) 
                                    cur.execute("UPDATE players SET gallery = ? WHERE id = ?", (cur.fetchone()[0]+1, msg.author.id,))
                                    con.commit()
                                    cur.execute("SELECT gallery5 FROM months WHERE id = ?", (msg.author.id,))
                                    cur.execute("UPDATE months SET gallery5 =? WHERE id = ?", (cur.fetchone()[0]+1, msg.author.id,))
                                    con.commit()
                            await ids_channel_property.send(str(msg.id) + "," + str(gallery_message.id))
                    else:
                        continue
                except Exception:
                    continue

    async def channels_func(ctx, self):
            cur.execute("SELECT prog FROM progi WHERE strefa=?",("pupile",))
            pupile_prog = cur.fetchone()[0]
            channels = {
                "strefa_selfies" : [
                    id_channel := ctx.bot.get_channel(1201517637197365319),
                    gallery_channel := ctx.bot.get_channel(497361494833496064),
                    selfies_channel := ctx.bot.get_channel(412146947412197396),
                    prog := 25,
                    text := "Galeria Strefy Selfies"
                ],

                "strefa_pupili" : [
                    pupile_ids_channel := ctx.bot.get_channel(1211334865954545694),
                    pupile_galeria := ctx.bot.get_channel(856870066175868968),
                    pupile_channel := ctx.bot.get_channel(412147918980644864),
                    prog := pupile_prog,
                    text := "Galeria Strefy Pupili"
                ],
                
                "strefa_kuchni" : [
                    kuchnia_ids_channel := ctx.bot.get_channel(1211334897713553539),
                    kuchnia_galeria := ctx.bot.get_channel(879843101626224741),
                    kuchnia_channel := ctx.bot.get_channel(412147997489627146),
                    prog :=7,
                    text := "Galeria Strefy Kuchni"
                ],

                "strefa_niesforna" : [
                    niesforna_ids_channel := ctx.bot.get_channel(1300506556315730011),
                    niesfor_galeria := ctx.bot.get_channel(1297947980573179934),
                    niesfor_channel := ctx.bot.get_channel(532659818071064586),
                    prog := 15,
                    text := "Galeria Strefy Niesfornej"
                ]
            }
            return channels

    @command()
    async def prog(ctx, self, num):
        cur.execute("UPDATE progi SET prog=? WHERE strefa=?", (num, "pupile",))
        con.commit()
        await self.send("Zmieniono próg")


    #@tasks.loop(time=gallery_times)
    async def gallery_checker(ctx, self, days_count=None):
        days_count = int(days_count) if days_count else 15
        
        channels = await listeners_tasks.channels_func(ctx, self)
        
        tday = (datetime.date.today() - datetime.timedelta(days=days_count)).day
        tmonth = (datetime.date.today() - datetime.timedelta(days=days_count)).month
        tyear = (datetime.date.today() - datetime.timedelta(days=days_count)).year
        
        CWD = Path(os.getcwd())
        counters = Path("grafiki/liczniki")
        for strefa in channels:
            if strefa != "strefa_selfies" and strefa != "strefa_pupili" and strefa != "strefa_niesforna":
                continue
            async for msg in channels[strefa][2].history(after=datetime.datetime(tyear, tmonth, tday)):
                form = 0
                if strefa == "strefa_pupili":
                    like_emoji = discord.utils.get(ctx.bot.emojis, name="serducho")
                else:
                    like_emoji = discord.utils.get(ctx.bot.emojis, name="like")
                reaction = discord.utils.get(msg.reactions, emoji=like_emoji)
                try:
                    if reaction.count >= channels[strefa][3]:
                        cur.execute("SELECT current_counter FROM players WHERE id = ?", (msg.author.id,))
                        counter = cur.fetchone()[0]
                        if strefa=="strefa_selfies":
                            print(counter)
                        if counter == None:
                            counter = "count_basic.png"
                        print("1")
                        path_to_counter = str(PurePath(CWD, counters, Path(counter)))
                        print("2")
                        attachment = msg.attachments[0]
                        e=discord.Embed(title=f"{msg.jump_url}", description=channels[strefa][4],color=discord.Color.yellow())
                        print("3")
                        e.set_image(url=attachment.url)
                        base = Image.open(fp = path_to_counter).convert("RGBA")
                        max_width =base.size[0]
                        print("4")
                        max_height =base.size[1]
                        txt = Image.new("RGBA", (max_width, max_height), (255,255,255,0))
                        draw = ImageDraw.Draw(txt)
                        fnt = ImageFont.truetype("AGENCYR.TTF", 290)
                        size = draw.textbbox(xy = (0,0),text=f"{reaction.count}", font=fnt)
                        wszerz = size[2]
                        draw.text(xy=((max_width-wszerz)/2,45), text=f"{reaction.count}", font=fnt, fill=(255,255,255,255))
                        out = Image.alpha_composite(base, txt)
                        e.set_author(name = f"{msg.author.name}", icon_url = msg.author.avatar.url)
                        async for message in channels[strefa][0].history(after=datetime.datetime(tyear, tmonth, tday)):
                            id_list = list(message.content.split(","))
                            if msg.id != int(id_list[0]):
                                continue
                            elif msg.id == int(id_list[0]):
                                form = 1 
                                gallery_message = await channels[strefa][1].fetch_message(int(id_list[1]))
                                with BytesIO() as file:
                                    out.save(file, format="PNG")
                                    file.seek(0)
                                    discord_file = discord.File(file, filename="image.png")
                                    e.set_thumbnail(url = "attachment://image.png")
                                    await gallery_message.edit(embed=e, attachments=[discord_file])
                        if form == 0:
                            with BytesIO() as file:
                                out.save(file, format="PNG")
                                file.seek(0)
                                discord_file = discord.File(file, filename="image.png")
                                e.set_thumbnail(url = "attachment://image.png")
                                if strefa=="strefa_niesforna":print("1")
                                gallery_message = await channels[strefa][1].send(embed=e, file=(discord_file))
                                if strefa == "strefa_selfies":
                                    cur.execute("SELECT gallery FROM players WHERE id = ?", (msg.author.id,)) 
                                    cur.execute("UPDATE players SET gallery = ? WHERE id = ?", (cur.fetchone()[0]+1, msg.author.id,))
                                    con.commit()
                                    cur.execute("SELECT gallery5 FROM months WHERE id = ?", (msg.author.id,))
                                    cur.execute("UPDATE months SET gallery5 =? WHERE id = ?", (cur.fetchone()[0]+1, msg.author.id,))
                                    con.commit()
                            await channels[strefa][0].send(str(msg.id) + "," + str(gallery_message.id))
                    else:
                        continue
                except Exception:
                    print("e")
    #tety licznika


    


    '''@command()
    async def usuwajto(ctx, self):
        channel = ctx.bot.get_channel(879843101626224741)
        async for msg in channel.history(limit=50):
            if msg.author.id== 1177286820556451880:
                await msg.delete()
'''
    #@Cog.listener("on_message")
    #async def zjeb_checker(self, message):
    #    if message.channel.id == 412156769561870338:
    #        if message.author.id in [337270418891079680, 418478883625500693]:
    #           await message.delete()


    @Cog.listener("on_message")
    async def adding_new_to_database(self, message):
        ver_channel_1 = self.bot.get_channel(494895117006667797)
        ver_channel_2 = self.bot.get_channel(1199385908517032026)
        ver_channel_3 = self.bot.get_channel(412146947412197396)
        niesforne_channel = self.bot.get_channel(487930372223401984)
        niesforne_photos_channel = self.bot.get_channel(532659818071064586)
        if message.channel.id in [ver_channel_1.id, ver_channel_2.id, ver_channel_3.id, niesforne_channel.id, niesforne_photos_channel.id]:
            cur.execute("INSERT OR IGNORE INTO players VALUES(?,?,?,?,?,?,?,?,?)",
                (
                    message.author.id,
                    message.author.name,
                    0,
                    0,
                    0,
                    0,
                    0,
                    "count_basic.png",
                    "profile_basic.png",
                ),)
            #cur.execute("INSERT OR IGNORE INTO months VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)", (message.author.id,0,0,0,0,0,0,0,0,0,0,0,0))
            con.commit()
            if message.channel.id == 412146947412197396 or message.channel.id == 1199385908517032026:
                if message.author.id != 1177286820556451880:
                    dupa = cur.execute("SELECT selfies FROM players WHERE id = ?", (message.author.id,)).fetchone()[0]
                    if dupa == 0:
                        await self.bot.get_channel(1179884652522115102).send(f"Rola atencjusz do przyznania: {message.author.mention}, {dupa} selfies, {message.author.id}")
                    
                    like_emoji = discord.utils.get(self.bot.emojis, name="like")
                    await message.add_reaction(str(like_emoji))
                    cur.execute(
                        "SELECT selfies FROM players WHERE id = ?", (message.author.id,)
                    )
                    cur.execute(
                        "UPDATE players SET selfies = ? WHERE id = ?",
                        (
                            cur.fetchone()[0] + 1,
                            message.author.id,
                        ),
                    )
                    con.commit()
            elif (message.channel.id == 1199385908517032026 or message.channel.id == 412146947412197396) and message.author.id !=1177286820556451880:
                like_emoji = discord.utils.get(self.bot.emojis, name="like")
                await message.add_reaction(str(like_emoji))

    
    
    @Cog.listener("on_raw_reaction_add")
    async def check_for_x(user, reaction):
        if (str(reaction.emoji) == "❌"
            and (reaction.channel_id == 963476559585505363 or reaction.channel_id == 1199385908517032026)
            and reaction.user_id == 742425630024400897):
            msg = await user.selfies_channel.fetch_message(reaction.message_id)
            cur.execute("SELECT selfies FROM players WHERE id = ?", (msg.author.id,))
            cur.execute(
                "UPDATE players SET selfies = ? WHERE id = ?",
                (
                    cur.fetchone()[0] - 1,
                    msg.author.id,
                ),
            )
            cur.execute("SELECT month5 FROM months WHERE id = ?", (msg.author.id,))
            cur.execute(
                "UPDATE months SET month5 = ? WHERE id = ?",
                (
                    cur.fetchone()[0] - 1,
                    msg.author.id,
                ),
            )
            con.commit()


    @Cog.listener("on_raw_reaction_add")
    async def like_act(self, payload: discord.RawReactionActionEvent):
        selfies_channel = self.bot.get_channel(412146947412197396)
        like_emoji = discord.utils.get(self.bot.emojis, name="like")
        if str(payload.emoji) == str(like_emoji) and (payload.channel_id == selfies_channel.id) and (payload.user_id != 1177286820556451880):
            msg = await selfies_channel.fetch_message(payload.message_id)
            cur.execute("SELECT likes FROM players WHERE id = ?", (msg.author.id,))
            current_likes = cur.fetchone()[0]
            cur.execute("UPDATE players SET likes = ? WHERE id = ?", (current_likes+1, msg.author.id,))
            con.commit()   

    @Cog.listener("on_raw_reaction_remove")
    async def like_remove(self, payload: discord.RawReactionActionEvent):
        selfies_channel = self.bot.get_channel(412146947412197396)
        like_emoji = discord.utils.get(self.bot.emojis, name="like")
        if str(payload.emoji) == str(like_emoji) and (payload.channel_id == selfies_channel.id) and (payload.user_id != 1177286820556451880):
            msg = await selfies_channel.fetch_message(payload.message_id)
            cur.execute("SELECT likes FROM players WHERE id = ?", (msg.author.id,))
            current_likes = cur.fetchone()[0]
            cur.execute("UPDATE players SET likes = ? WHERE id = ?", (current_likes-1, msg.author.id,))
            con.commit()  
            
    @Cog.listener("on_message")
    async def thread_adder(self, message):
        if message.channel.id == 412146947412197396 or message.channel.id == 1199385908517032026 or message.channel.id == 532659818071064586:
            if message.author.id != 1177286820556451880:
                await message.create_thread(name=f"Komentarze: {message.author.name}", auto_archive_duration = 10080)
        elif message.channel.id == 1171195189205946499:
            if message.author.id != 1177286820556451880:
                await message.create_thread(name=f"Komentarze:", auto_archive_duration=10080)





async def setup(bot: Bot):
    await bot.add_cog(listeners_tasks(bot))









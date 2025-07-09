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
import math


con = sqlite3.connect('data/selfies_database.db')
con.row_factory = sqlite3.Row
cur = con.cursor()

birthday_time = datetime.time(hour=11,tzinfo=ZoneInfo("Europe/Warsaw"))



class birthday(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot


    @tasks.loop(time=birthday_time)
    async def birthday_checker(ctx, self):
        birthday_role = discord.utils.get(self.guild.roles, id = 1250518611114721312)
        urodziny_channel = ctx.bot.get_channel(628530693386797076)
        td_month = (t.strftime("%m"))
        td_day = (t.strftime("%d"))
        date = td_month+"-"+td_day
        cur.execute("SELECT user_id FROM birthdays WHERE date = ? AND done = ?", (date,0))
        wynik = cur.fetchall()
        if wynik is None: 
            return
        else:
            for user in wynik:
                if user is None:
                    continue
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
    async def birthday_manual_checker(ctx, self):
        birthday_role = discord.utils.get(self.guild.roles, id = 1250518611114721312)
        urodziny_channel = ctx.bot.get_channel(628530693386797076)
        td_month = (t.strftime("%m"))
        td_day = (t.strftime("%d"))
        date = td_month+"-"+td_day
        cur.execute("SELECT user_id FROM birthdays WHERE date = ? AND done = ?", (date,0))
        wynik = cur.fetchall()
        if wynik is None: 
            return
        else:
            for user in wynik:
                if user is None:
                    continue
                member = ctx.bot.get_user(user[0])
                if member is None:
                    continue
                else:
                    out, texts, path_to_avatar = birthday.birthday_message_maker(ctx, self, member) 
                    with BytesIO() as file:
                        out.save(file, format="PNG")
                        file.seek(0)
                        discord_file = discord.File(file, filename="image.png")
                        await urodziny_channel.send(content = texts[random.randint(0, 3)], file=discord_file)
                    cur.execute("UPDATE birthdays SET done=? WHERE user_id = ?", (1, user[0],))
                    con.commit()
                    os.remove(path_to_avatar)

    
    async def birthday_message_maker(ctx, self, member):
        CWD = Path(os.getcwd())
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
        return out, texts, path_to_avatar


    @command()
    async def b_add(ctx, self, id:int, date:str):
        if self.author.id == 742425630024400897:
            cur.execute("INSERT INTO birthdays VALUES(?,?,?)", (id, date, 0))
            con.commit()    
            print("done")
    
    @app_commands.command(name="urodziny", description="Komenda pozwalająca dodawać lub usuwać swoją datę urodzin")
    @app_commands.describe(opcja="Wybierz co chcesz zrobić", 
                           dzień = "Wpisz dzień urodzenia (liczbę)",
                           miesiąc = "Wybierz miesiąc urodzenia"
                           )
    async def schedule(self, interaction: discord.Interaction, opcja:Literal["dodaj datę urodzenia", "usuń datę urodzenia"], miesiąc:Literal["Styczeń", "Luty", "Marzec", "Kwiecień", "Maj", "Czerwiec","Lipiec","Sierpień","Wrzesień","Październik","Listopad","Grudzień"]=None,  dzień:int=None):
        if opcja == "dodaj datę urodzenia" and dzień is not None and miesiąc is not None:
            months_dict = {"Styczeń":"01", "Luty":"02", "Marzec":"03", "Kwiecień":"04", "Maj":"05", "Czerwiec":"06",
                           "Lipiec":"07","Sierpień":"08","Wrzesień":"09","Październik":"10","Listopad":"11","Grudzień":"12"}
            if dzień < 10:
                dzień = f"0{dzień}"
            cur.execute("SELECT EXISTS(SELECT 1 FROM birthdays WHERE user_id = ?)", (interaction.user.id,))
            if cur.fetchone()[0]:
                cur.execute("UPDATE birthdays SET date=? WHERE user_id=?", (f"{months_dict[miesiąc]}-{dzień}", interaction.user.id))
                con.commit()
                await interaction.response.send_message(f"Zmieniono datę Twoich urodzin: ``{dzień} {miesiąc}``", ephemeral=True)
            else:
                cur.execute("INSERT OR IGNORE INTO birthdays VALUES(?,?,?)", (interaction.user.id,f"{months_dict[miesiąc]}-{dzień}",0))
                con.commit()
                await interaction.response.send_message("Dodano Twoje urodziny! :3", ephemeral=True)
        elif opcja == "dodaj datę urodzenia" and dzień is None and miesiąc is None:
            await interaction.response.send_message("Pamiętaj o wpisaniu mięsiąca i dnia swoich urodzin!", ephemeral=True)
        elif opcja == "usuń datę urodzenia":
            cur.execute("DELETE FROM birthdays WHERE user_id = ?", (interaction.user.id,))
            con.commit()
            await interaction.response.send_message("Usunięto datę Twoich urodzin!", ephemeral=True)
    
    
    @app_commands.command(name="urodziny_lista", description="Komenda wyświetlająca listę dat urodzin Stratowiczów!")
    async def _lista_urodzin(self, interaction: discord.Interaction):
        cur.execute(f"SELECT * FROM birthdays ORDER BY date ASC")
        items = cur.fetchall()     
        users_string = ""   
        for record in items[0:10]:
            date_list = [i for i in record[1].split("-")]
            try:
                user_name = await interaction.guild.fetch_member(record[0])
            except Exception:
                    continue
            users_string = users_string + f"`{user_name}`: {date_list[0]}.{date_list[1]}\n"
        pages = math.ceil(len(items) / 10)
        e=discord.Embed(title=f"Spis urodzin", description=f"{users_string}",color=discord.Color.yellow())
        e.set_footer(text=f"Strona 1/{pages}")
        await interaction.response.send_message(embed=e, view=birthday.BirthsButtons())
    
    class BirthsButtons(discord.ui.View):
        def __init__(self):
            self.page = 1
            cur.execute(f"SELECT * FROM birthdays ORDER BY date ASC")
            self.items = cur.fetchall()
            self.pages = math.ceil(len(self.items) / 10)
            super().__init__(timeout=None)
        
        @discord.ui.button(label='', style=discord.ButtonStyle.green, emoji='◀️')              
        async def receive2(self, interaction:discord.Interaction, button1: discord.ui.Button):
            if self.page==1:
                self.page=self.pages
            elif self.page==None:
                self.page=self.pages
            else:
                self.page-=1
            
            users_string = ""
            for record in self.items[(self.page-1)*10:10*(self.page)]:
                try:
                    date_list = [i for i in record[1].split("-")]
                    user_name = await interaction.guild.fetch_member(record[0])
                    users_string = users_string + f"**{user_name}**: {date_list[0]}.{date_list[1]}\n"
                except Exception:
                    continue
            e=discord.Embed(title=f"Spis urodzin", description=f"{users_string}",color=discord.Color.yellow())
            e.set_footer(text=f"Page {self.page}/{self.pages}")
           
            await interaction.response.edit_message(content="",embed=e,attachments="")
                

        @discord.ui.button(label='', style=discord.ButtonStyle.green, emoji="▶️")
        async def receive(self, interaction: discord.Interaction,button: discord.ui.Button):    
            if self.page==self.pages:
                self.page=self.pages-(self.pages-1)
            elif self.page==None:
                self.page=1
            else:
                self.page+=1
            
            users_string = ""
            for record in self.items[(self.page-1)*10:10*(self.page)]:
                try:
                    date_list = [i for i in record[1].split("-")]
                    user_name = await interaction.guild.fetch_member(record[0])
                    users_string = users_string + f"**{user_name}**: {date_list[0]}.{date_list[1]}\n"
                except Exception:
                    continue

            e=discord.Embed(title=f"Spis urodzin", description=f"{users_string}",color=discord.Color.yellow())
            e.set_footer(text=f"Page {self.page}/{self.pages}")
    
            await interaction.response.edit_message(embed=e, view=self, attachments="")
            
    
    @command()
    async def urodziny(ctx, self, opcja:str, member:discord.Member):
        cur.execute("SELECT month, day FROM birthdays WHERE user_id = ?", (member.id,))
        wynik = cur.fetchall()
        if self.author.id == 742425630024400897 and wynik is not None:
            if opcja == "usun":
                cur.execute("DELETE FROM birthdays WHERE user_id = ?", (member.id,))
                con.commit()
            elif opcja == "sprawdz":
                await self.send(f"{member.name}: {wynik[0][0]}, {wynik[0][1]}")
        else:
            await self.send("Nie masz uprawnień :(")
    
    async def is_cedi(ctx, self, id):
        self.bot.get_user(id)


async def setup(bot: Bot):
    await bot.add_cog(birthday(bot))

        

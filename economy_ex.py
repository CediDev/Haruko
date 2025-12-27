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
from zoneinfo import ZoneInfo
import math
from pathlib import Path, PurePath
import inspect
import requests

con = sqlite3.connect('data/selfies_database.db')
con.row_factory = sqlite3.Row
cur = con.cursor()


utc = datetime.timezone.utc
time = datetime.time(hour=22, minute=45, tzinfo=utc)



no_perm_embed = discord.Embed(title="Nie posiadasz permisji!", description="", color=discord.Colour.red())

class economy_ex(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    dupa = "dupa"

    def archiver(func):
        async def wrapper(self, *args, **kwargs):
            function = await func(args, kwargs)
            date = t.strftime("%Y-%m-%d %H:%M")
            raport_channel = self.bot.get_channel(1188542888989163620)
            await raport_channel.send(f"{date} | {func.__name__}: {list(args)}, {list(kwargs)}, {function}")
        wrapper.__name__ = func.__name__
        sig = inspect.signature(func)
        wrapper.__signature__ = sig.replace(parameters=tuple(sig.parameters.values())[1:])
        return wrapper
    
    
    @command()
    async def close_connection(ctx, self):
        con.close()

    @command()
    async def b_database_restart(self, ctx):
        cur.execute("UPDATE birthdays SET done = ?", (1,))
        con.commit()
        print("done")

    #sticky message
    
    @Cog.listener("on_message")
    async def sticky_mess_selfies(self, message):
        selfies_channel = self.bot.get_channel(762068995028549684)
        selfies_bot_channel = self.bot.get_channel(1179884652522115102)
        self.raport_channel = self.bot.get_channel(1188542888989163620)
        selfies_for_noobs = self.bot.get_channel(1199385908517032026)
        sticky_message_channel = self.bot.get_channel(1203338155617554504)
        if message.channel.id == selfies_for_noobs.id and message.author.id != 1177286820556451880: 
            OK_user = message.guild.get_member(742425630024400897)
            embed = discord.Embed(title = "Witaj na kanale #selfies!",description=f"Za wysłane zdjęcia otrzymasz punkty oraz rolę Atencjusz za pierwsze z nich. Po zdobyciu 10 poziomu na bocie Bruno uzyskasz dostęp do kanału {selfies_channel.jump_url} (#selfies_plus), gdzie można zdobyć więcej punktów! W przypadku pytań lub problemów pisz proszę do Opiekunki Kanału: {OK_user.mention}", colour=discord.Colour.pink())
            try:
                async for msg in sticky_message_channel.history(limit=1):
                    id = msg.content
                    mess_to_delete = await selfies_for_noobs.fetch_message(int(id))
                    await mess_to_delete.delete()
            except Exception:
                pass
            sticky_mess = await selfies_for_noobs.send(embed=embed)
            await sticky_message_channel.send(sticky_mess.id)
    
    @Cog.listener("on_message")
    async def sticky_mess_anno(self, message):
        if message.channel.id == 1216764806162415726 and message.author.id != 1177286820556451880:
            id_channel = self.bot.get_channel(1216770475988881498) 
            selfies_for_noobs = self.bot.get_channel(1199385908517032026) 
            selfies_channel = self.bot.get_channel(412146947412197396)  
            anno_channel = self.bot.get_channel(1216764806162415726)
            embed = discord.Embed(title="Witaj na kanale ogłoszeń Strefy Selfies!", description=f"Tutaj znajdziesz najważniejsze informacje dotyczące zmian i aktualizacji. Jeśli szukasz punktacji bądź zasad, znajdziesz je w przypiętych wiadomościach na {selfies_for_noobs.jump_url} oraz {selfies_channel.jump_url} `(selfies_plus)`", colour=discord.Colour.green())
            try:
                async for msg in id_channel.history(limit=1):
                    id = msg.content
                    mess_to_delete = await anno_channel.fetch_message(int(id))
                    await mess_to_delete.delete()
            except Exception:
                pass
            sticky_mess = await anno_channel.send(embed=embed)
            await id_channel.send(sticky_mess.id)
    
    '''@Cog.listener()
    async def on_message(self, message):
        selfies_channel = self.bot.get_channel(412146947412197396)
        selfies_bot_channel = self.bot.get_channel(1179884652522115102)
        self.raport_channel = self.bot.get_channel(1188542888989163620)
        selfies_for_noobs = self.bot.get_channel(1199385908517032026)
        sec_sticky_mess_channel = self.bot.get_channel(1215973508081782955)
        third = self.bot.get_channel(1215977805733695679)
        selfies_komentarze = self.bot.get_channel(494895117006667797)
        cedi = message.guild.get_member(742425630024400897)
        ankieta_message = await selfies_komentarze.fetch_message(1215976462285279372)
        if message.channel.id == selfies_channel.id and message.author.id != 1177286820556451880:   
            embed = discord.Embed(title = "Ogłoszenie",description=f"Hej! W przerwie od oglądania selfiaków (bądź też wysyłania swoich) prosiłabym o wypełnienie ankiety (**tylko jedno pytanie**) dotyczącej rozwoju Strefy Selfies ({ankieta_message.jump_url}). Po zagłosowaniu będziecie mieli szansę wygrać **10000 **punktów serwerowych w losowaniu!", colour=discord.Colour.green())
            try:
                async for msg in third.history(limit=1):
                    id = msg.content
                    mess_to_delete = await selfies_channel.fetch_message(int(id))
                    await mess_to_delete.delete()
            except Exception:
                pass
            sticky_mess = await selfies_channel.send(embed=embed)
            await third.send(sticky_mess.id)
        if message.channel.id == selfies_for_noobs.id and message.author.id != 1177286820556451880: 
            embed = discord.Embed(title = "Ogłoszenie",description=f"Hej! W przerwie od oglądania selfiaków (bądź też wysyłania swoich) prosiłabym o wypełnienie ankiety (**tylko jedno pytanie**) dotyczącej rozwoju Strefy Selfies ({ankieta_message.jump_url}). Po zagłosowaniu będziecie mieli szansę wygrać **10000 **punktów serwerowych w losowaniu!", colour=discord.Colour.green())
            try:
                async for msg in sec_sticky_mess_channel.history(limit=1):
                    id = msg.content
                    mess_to_delete = await selfies_for_noobs.fetch_message(int(id))
                    await mess_to_delete.delete()
            except Exception:
                pass
            sticky_mess = await selfies_for_noobs.send(embed=embed)
            await sec_sticky_mess_channel.send(sticky_mess.id)'''

    
    class HelpSelect(discord.ui.Select):
        def __init__(self):
            # Set the options that will be presented inside the dropdown
            options = [
                discord.SelectOption(
                    label="Ekonomia i waluta",
                    description="Wyjaśnienie dotyczące działania systemu ekonomii",
                    emoji="💎",
                ),
                discord.SelectOption(
                    label="Osiągnięcia",
                    description="Przedstawienie nowej funkcjonalności - osiągnięć!",
                    emoji="🏆",
                ),
                discord.SelectOption(
                    label="Questy", description="Proste zadania od Opiekunki Strefy Selfies",
                    emoji="🎯"
                ),
                discord.SelectOption(
                    label="Gambling",
                    description="Ryzykuj monetami by wygrać! ...lub przegrać",
                    emoji="🎲"
                )
            ]
            super().__init__(
                placeholder="Wybierz kategorię...",
                min_values=1,
                max_values=1,
                options=options,
            )

        async def callback(self, interaction: discord.Interaction):
            if self.values[0] == "Ekonomia i waluta":
                embed = discord.Embed(title="Ekonomia i waluta", colour=discord.Colour.pink())
                embed.add_field(
                    name="Jak zdobywać monety?",
                    value="Monety to nowa i ekskluzywna dla Strefy Selfies Waluta."
                    + " Zdobywa się ją poprzez wykonywanie cotygodniowych zadań, zdobywanie Achievementów oraz wysyłanie selfies.",
                )
                embed.add_field(
                    name="Jak mogę je wykorzystać?",
                    value="Za monety będzie można kupić rzeczy kosmetyczne (profile i liczniki). Ewentualnie możesz je wymienić na punkty serwerowe."
                    + " W przyszłości planowane jest dodanie innych zastosowań monet - stay tuned ;3",
                    inline=False
                )
                embed.add_field(
                    name="Powiązane komendy",
                    value="- **coins** `ilość` `@użytkownik` **(administracyjna)**"
                    + "\n- **przekaz** `ilość` `@użytkownik`",
                    inline=False
                )
                await interaction.response.send_message(embed=embed)
            if self.values[0] == "Osiągnięcia":
                embed = discord.Embed(title="Osiągnięcia", colour=discord.Colour.pink())
                embed.add_field(
                    name="Czym one są?",
                    value="Jest to nowa forma pobocznych zadań w obrębie Strefy Selfies. Po zdobyciu kolejnych poziomów danego osiągnięcia można zgłosić się do Opiekunki Strefy Selfies po nagrodę :)",
                )
                embed.add_field(
                    name = "Przyszłość osiągnięć",
                    value = "Planuję dodać odznaki (badge) do profili, które będzie można zdobyć także za osiągnięcia.",
                    inline=False
                )
                embed.add_field(
                    name="Powiązane komendy",
                    value="- **osiagniecia** `@użytkownik`"
                    + "\nSzczegóły dostępne są pod komendą /komendy",
                    inline=False
                )
                await interaction.response.send_message(embed=embed)
            if self.values[0] == "Questy":
                embed = discord.Embed(title="Questy", colour=discord.Colour.pink())
                embed.add_field(
                    name="Czym one są?",
                    value="Questy to aktywna forma zadań w obrębie Strefy Selfies."
                    + " Są one tworzone przez Opiekunkę Strefy i posiadają konkretny termin, wymagania oraz nagrodę.",
                )
                embed.add_field(
                    name="Powiązane komendy",
                    value="- **/apply** `ID questa` `link do wiadomości`"
                    + "\n- **/quest** `nagroda` `termin` `opis` **(administracyjna)**"
                    + "\nSzczegóły dostępne są pod komendą /komendy",
                    inline=False
                )
                await interaction.response.send_message(embed=embed)
            if self.values[0] == "Gambling":
                embed = discord.Embed(title="Gambling", colour=discord.Colour.pink())
                embed.add_field(name="Powiązane komendy", value= "**gamble** `ilość monet`"
                                + "\nSzczegóły dostępne są pod komendą /komendy")
                embed.add_field(name="Poszczególne szanse", value="\n**1%** - Strata całości"
                        +"\n**30%** - Strata połowy"
                        +"\n**30%** - Mnożnik x1 (brak wygranej, brak straty)"
                        +"\n**33%** - Mnożnik x2"
                        +"\n**5%** - Mnożnik x3"
                        +"\n**1%** - Mnożnik x5")
                await interaction.response.send_message(embed=embed)

    
    
    class HelpSelectView(discord.ui.View):
        def __init__(self):
            super().__init__()

            # Adds the dropdown to our view object.
            self.add_item(economy_ex.HelpSelect())

    @command()
    async def pomoc(ctx, self):
        view = economy_ex.HelpSelectView()
        await self.author.send(view=view)

    
    @command()
    async def osiagniecia(ctx, self, member:discord.Member = None):
        if member == None:
            member = self.author
        questy = {
            "Piękniś": [10, 20, 35, 75, 100, 150, 250, 500, 750],
            "Atencjusz": [25, 50, 80, 125, 200, 500, 750, 1000, 1500, 2000, 3000, 5000],
            "Kolekcjoner": [5, 10, 20, 30, 50],
        }
        embed = discord.Embed(title="", description="Lista Twoich osiągnięć")

        def value_check(namel, count):
            for iteration, i in enumerate(questy[namel], start=1):
                if i <= count:
                    continue
                elif i > count:
                    return iteration, i

        cur.execute("SELECT gallery FROM players WHERE id = ?", (member.id,))
        gallery_count = cur.fetchone()[0]
        gallery_data = value_check("Piękniś", gallery_count)
        embed.add_field(
            name="Piękniś" + f" {gallery_data[0]}",
            value=f"Spraw, aby {gallery_data[1]} Twoich zdjęć znalazło się w galerii.\n**{gallery_count}/{gallery_data[1]}** ({int((gallery_count/gallery_data[1])*100)}%)",
        )

        cur.execute("SELECT selfies FROM players WHERE id = ?", (member.id,))
        selfies_count = cur.fetchone()[0]
        selfies_data = value_check("Atencjusz", selfies_count)
        embed.add_field(
            name="Atencjusz" + f" {selfies_data[0]}",
            value=f"Wyślij {selfies_data[1]} selfiaków.\n**{selfies_count}/{selfies_data[1]}** ({int((selfies_count/selfies_data[1])*100)}%)",
            inline=False,
        )

        cur.execute("SELECT Items FROM players WHERE id = ?", (member.id,))
        items_count = cur.fetchone()[0]
        items_data = value_check("Kolekcjoner", items_count)
        embed.add_field(
            name="Kolekcjoner" + f" {items_data[0]}",
            value=f"Kup {items_data[1]} motywów ze sklepu Strefy Selfies.\n**{items_count}/{items_data[1]}** ({int((items_count/items_data[1])*100)}%)",
        )

        await self.send(embed=embed)

    
    @app_commands.command(name="zgloszenie",description="Tutaj możesz zgłosić jakąś sprawę dotyczącą bota bezpośrednio do Opiekunki Strefy Selfies.")
    @app_commands.describe(type="Wybierz typ sprawy", description="Dokładnie opisz powód zgłoszenia")
    async def report_func(self, interaction: discord.Interaction, type: Literal["Bug", "Sugestia", "Inne"], description: str,):
        raport_channel = self.bot.get_channel(1188542888989163620)
        date = t.strftime("%Y-%m-%d %H:%M")
        selfies_bot = self.bot.get_channel(1179884652522115102)
        await selfies_bot.send(
            f"{interaction.user.name} | ID zgłoszenia: {interaction.id}\
                           \n- Typ: **{type}**\n{description}"
        )
        await raport_channel.send(
            f"{date} | {interaction.user.name} | ID zgłoszenia: {interaction.id}\
                           \n- Typ: **{type}**\n{description}"
        )
        await interaction.response.send_message(
            "Wiadomość wysłana. Dziękuję za zgłoszenie i proszę o cierpliwość w sprawie odpowiedzi!",
            ephemeral=True,
        )


    @command()
    async def database_writer(ctx, self, table:str):
        query = "SELECT * FROM {}".format((table))
        cur.execute(query)
        for i in cur.fetchall():
            rec_string = ""
            for j in i: rec_string = rec_string + f"{j}, "
            print(rec_string)

    
    @app_commands.command(name="prezent", description="Służy do odbioru jednorazowego prezentu dla nowych użytkowników!")
    async def prezent_response(self, interaction:discord.Interaction):
        cur.execute("SELECT user_id FROM prezenty WHERE user_id = ?", (interaction.user.id,))
        if cur.fetchone() is not None:     
            await interaction.response.send_message("Już odebrałxś swój prezent!")    
        else:
            new_user_role = discord.utils.get(interaction.guild.roles, id=412357250401697794)
            ticket_channel = self.bot.get_channel(1213901611836117052)
            if new_user_role not in interaction.user.roles:
                await interaction.response.send_message("Do tej komendy mają dostęp tylko osoby z rolą `Nowy`!")
            else:
                chances = {
                    "1000 punktów" : 0.50,
                    "3000 punktów" : 0.30,
                    "5000 punktów" : 0.10,
                    "Własny kolor nicku na 14 dni" : 0.07,
                    "Losowa gra na Steam" : 0.03
                }
                items = [item for item in chances.keys()]
                items_chances = [chance for chance in chances.values()]
                prize = random.choices(population=items, weights=items_chances, k=1)
                CWD = Path(os.getcwd())
                path_to_main_image = str(PurePath(CWD, Path("gift_image.png")))
                main_img = Image.open(fp=path_to_main_image).convert("RGBA")
                embed = discord.Embed(title=f"Prezent", description=f"Wow {interaction.user.mention}! Wygrałxś właśnie **{prize[0]}**, gratuluję!\nAby odebrać nagrodę wejdź na {ticket_channel.jump_url}, otwórz ticket klikając przycisk z ikonką prezentu, a potem wyślij na utworzonym kanale screenshot tej wiadomości.")
                with BytesIO() as file:
                    main_img.save(file, format="PNG")
                    file.seek(0)
                    discord_file = discord.File(file, filename="image.png")
                    embed.set_image(url="attachment://image.png")
                    await interaction.response.send_message(embed=embed, file=discord_file)
                cur.execute("INSERT INTO prezenty VALUES(?)", (interaction.user.id,))
                con.commit()
    
    @command()
    async def birth_delete(ctx, self, id):
        cur.execute("DELETE FROM prezenty WHERE user_id = ?", (id,))        
        con.commit()
    
    
    @command()
    async def sync(ctx, self):
        print("done")
        await self.bot.tree.sync(guild = discord.Object(id = 211261411119202305))
        await self.bot.tree.sync(guild = discord.Object(id = 963476559585505360))

    @command()
    async def test_sync(ctx, self):
        print("done")
        await self.bot.tree.sync(guild= discord.Object(id=963476559585505360))




    @command()
    async def komendy(ctx, self):
        embed1 = discord.Embed(
            title="Ekonomia i profile", description="", colour=discord.Colour.pink()
        )
        embed1.add_field(
            name="- **coins** `ilość` `@użytkownik` **(administracyjna)**",
            value=" *dodaje lub odejmuje monety danemu użytkowniowi*",
        )
        embed1.add_field(
            name="- **przekaz** `ilość` `@użytkownik`",
            value="*przekazuje daną ilość monet innemu użytkownikowi*",
            inline=False,
        )
        embed1.add_field(
            name="- **profil** `@użytkownik`",
            value="*pokazuje profil danego usera; w przypadku braku wzmianki pokazuje profil osoby wysyłającej komendę*",
            inline=False,
        )
        embed1.add_field(
            name="- **osiagniecia** `@użytkownik`",
            value="*pokazuje osiągnięcia danego usera i ich postęp; w przypadku braku wzmianki pokazuje osiągnięcia osoby wysyłającej komendę*",
            inline=False,
        )

        embed2 = discord.Embed(
            title="Questy", description="", colour=discord.Colour.pink()
        )
        embed2.add_field(
            name="- **/quest** `nagroda` `termin` `opis` **(administracyjna)**",
            value="*Tworzy konkretnego questa*",
        )
        embed2.add_field(
            name="- **/apply** `ID questa` `link do wiadomości`",
            value=" *wysyła zgłoszenie do danego questa*",
            inline=False,
        )
        embed3=discord.Embed(
            title="Gambling", description="", colour=discord.Colour.pink()
        )
        embed3.add_field(
            name="**- gamble** `ilość monet`",
            value="Losuje podaną ilość monet z następującymi szansami:"
            +"\n**1%** - Strata całości"
            +"\n**30%** - Strata połowy"
            +"\n**30%** - Mnożnik x1 (brak wygranej, brak straty)"
            +"\n**33%** - Mnożnik x2"
            +"\n**5%** - Mnożnik x3"
            +"\n**1%** - Mnożnik x5"
        )
        embed4=discord.Embed(
            title="Sklep", colour=discord.Colour.pink())
        embed4.add_field(name="- **sklep** `liczniki/profile`", value="Wyświetla obecnie dostępne liczniki i profile, ich cenę oraz ID")
        embed4.add_field(name="- **kup** `profil/licznik` `id`", value = "*Kupuje licznik/profil o danym ID (do sprawdzenia w sklepie)*",
                         inline=False)
        embed4.add_field(name="- **set** `licznik/profil` `ID`", value="Ustawia dany licznik lub profil, o ile masz go zakupionego.")
        await self.author.send(embeds=[embed1, embed2, embed3, embed4])

    '''async def streak_counter(channel, user):
        today_date = str(
            datetime.datetime(
                int(t.strftime("%Y")), int(t.strftime("%m")), int(t.strftime("%d"))
            )
        )
        ddd = [int(today_date[5:7]), int(today_date[8:10])]
        daily_count = 0
        send_status = "Niewysłane"
        text = False
        is_done = False
        yesterday = [int(today_date[5:7]), int(today_date[8:10]) - 1]
        async for msg in channel.history(limit=100):
            if msg.author.id == user:
                msg_created_at = str(msg.created_at)
                msg_month_and_day = [
                    int(msg_created_at[5:7]),
                    int(msg_created_at[8:10]),
                ]
                if ddd == msg_month_and_day:
                    send_status = "Wysłane"
                    text = True
            else:
                continue
        async for msg in channel.history(limit=100):
            if msg.author.id == user:
                msg_created_at = str(msg.created_at)
                msg_month_and_day = [
                    int(msg_created_at[5:7]),
                    int(msg_created_at[8:10]),
                ]

                if ddd == msg_month_and_day:
                    daily_count += 1
                    ddd[1] = ddd[1] - 1
                    is_done = True
                elif (
                    (ddd != msg_month_and_day)
                    and (yesterday == msg_month_and_day)
                    and (is_done == False)
                ):
                    daily_count += 1
                    ddd[1] = ddd[1] - 2
                    is_done = True
                else:
                    continue
            else:
                continue

        return [daily_count, send_status, text]

    @command()
    async def daily(ctx, self):
        daily_count, send_status, text = await economy_ex.streak_counter(self.selfies_channel, self.author.id)

        blank_emoji = discord.utils.get(self.bot.emojis, name="blank_emoji")
        full_emoji = discord.utils.get(self.bot.emojis, name="full_emoji")

        blank_spaces = 10 - daily_count
        streak_progress_str = daily_count * str(full_emoji) + blank_spaces * str(
            blank_emoji
        )

        embed = discord.Embed(title="", description="", colour=discord.Colour.pink())
        embed.add_field(
            name=f"Obecny streak: `{daily_count}/10`!", value=f"{streak_progress_str}"
        )
        if text == True:
            embed.add_field(
                name=f"Dzisiejsze zdjęcie: `{send_status}`",
                value=f"Jutrzejszy bonus: {daily_count*5 +5}",
                inline=False,
            )
        elif text == False:
            embed.add_field(
                name=f"Dzisiejsze zdjęcie: `{send_status}`",
                value=f"Dzisiejszy bonus: {daily_count*5 +5}",
                inline=False,
            )
        embed.set_footer(text="Daily resetuje się codziennie o 24:00!")
        await self.send(embed=embed)

    @Cog.listener("on_message")
    async def streak_listener(self, message):
        selfies_channel = self.bot.get_channel(412146947412197396)
        selfies_bot_channel = self.bot.get_channel(1179884652522115102)
        self.raport_channel = self.bot.get_channel(1188542888989163620)
        selfies_for_noobs = self.bot.get_channel(1199385908517032026)
        sticky_message_channel = self.bot.get_channel(1203338155617554504)
        user = message.author.id
        num = 0
        full_emoji = discord.utils.get(self.bot.emojis, name="arrow_right")
        if (
            message.channel.id == selfies_channel.id
            and message.author.id != 1177286820556451880
        ):
            daily_count = await economy_ex.streak_counter(selfies_channel, user)
            count = daily_count[0]
            yday = datetime.date.today().day
            ymonth = datetime.date.today().month
            yyear = datetime.date.today().year
            tday = (datetime.date.today() + datetime.timedelta(days=1)).day
            tmonth = (datetime.date.today() + datetime.timedelta(days=1)).month
            tyear = (datetime.date.today() + datetime.timedelta(days=1)).year
            async for msg in selfies_channel.history(
                limit=50,
                after=datetime.datetime(yyear, ymonth, yday),
                before=datetime.datetime(tyear, tmonth, tday),
            ):
                if msg.author.id == message.author.id:
                    num += 1
            points_to_add = count * 5
            if num == 1:
                e = discord.Embed(
                    title="Daily Streak!", description="", colour=discord.Colour.pink()
                )
                e.add_field(
                    name=f"{full_emoji} Bonusowe monety za`{count}` dni streaka!",
                    value=f"Bonus: `{points_to_add}`",
                )
                message_to_delete = await selfies_channel.send(
                    f"{message.author.mention}", embed=e
                )
                await asyncio.sleep(7)
                await message_to_delete.delete()
                cur.execute(
                    "SELECT coins FROM players WHERE id = ?", (message.author.id,)
                )
                coins = cur.fetchone()[0]
                date = t.strftime("%Y-%m-%d %H:%M")
                await self.raport_channel.send(
                    f"{date} | {message.author.name} otrzymał* {points_to_add} Streak Bonusu | Saldo przed: {coins} | Saldo po: {coins+points_to_add}"
                )
                cur.execute("UPDATE players SET coins = ? WHERE id = ?", (points_to_add + coins, message.author.id,))
                con.commit()'''


    @command()
    async def coins(ctx, self, member: discord.Member, amount: int):
        date = t.strftime("%Y-%m-%d %H:%M")
        if self.author.id == 742425630024400897:
            cur.execute("SELECT coins FROM players WHERE id = ?", (member.id,))
            coins_amount = cur.fetchone()[0]
            cur.execute(
                "UPDATE players SET coins = ? WHERE id = ?",
                (
                    coins_amount + amount,
                    member.id,
                ),
            )
            con.commit()
            if amount > 0:
                await self.send(f"Przyznano {amount} monet użytkownikowi {member.name}")
            elif amount < 0:
                await self.send(f"Odebrano {-amount} monet użytkownikowi {member.name}")
            await ctx.raport_channel.send(
                f"{date} | {member.name} otrzymał* {amount} monet od {self.author.name} | Saldo przed: {coins_amount} | Saldo po: {coins_amount+amount}"
            )
        else:
            await self.send(embed=no_perm_embed)

    @command()
    async def przekaz(ctx, self, member: discord.Member, amount: int):
        date = t.strftime("%Y-%m-%d %H:%M")
        cur.execute("SELECT coins FROM players WHERE id = ?", (self.author.id,))
        player_coins_amount = cur.fetchone()[0]
        if (
            player_coins_amount >= amount
            and amount >= 0
            and member.id != self.author.id
        ):
            cur.execute("SELECT coins FROM players WHERE id = ?", (member.id,))
            receiving_coins_amount = cur.fetchone()[0]
            cur.execute(
                "UPDATE players SET coins = ? WHERE id = ?",
                (
                    receiving_coins_amount + amount,
                    member.id,
                ),
            )
            await self.send(f"Przekazano {amount} punktów dla {member.name}")
            await ctx.raport_channel.send(
                f"{date} | {self.author.name} przekazał {amount} punktów dla {member.name} | Saldo wysyłającego przed: {player_coins_amount} | Saldo wysyłającego po: {player_coins_amount-amount} | Saldo otrzymującego przed: {receiving_coins_amount} | Saldo otrzymującego po: {receiving_coins_amount + amount}"
            )
        else:
            await self.send(
                "Upewnij się, że dobrze wpisałeś komendę i masz wystarczającą ilość monet!!!"
            )

    '''@command()
    async def gallery_sim(ctx, self):

        CWD = Path(os.getcwd())
        counters = Path("grafiki/liczniki")
        randomlike = random.randint(15, 30)
        con = sqlite3.connect("selfies_database.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        cur.execute(
            "SELECT current_counter FROM players WHERE id = ?", (self.author.id,)
        )
        scounter = cur.fetchone()[0]
        counter = PurePath(CWD, counters, scounter)
        cur.execute("SELECT color FROM counters WHERE url = ?", (scounter,))
        colore = cur.fetchone()[0]

        e = discord.Embed(
            title=f"{self.message.jump_url}",
            description=f"Galeria - Listopad",
            color=discord.Colour.from_str(f"#{colore}"),
        )
        e.set_image(url=self.author.avatar.url)
        base = Image.open(counter.strip('"')).convert("RGBA")
        max_width = base.size[0]
        max_height = base.size[1]
        txt = Image.new("RGBA", (max_width, max_height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt)
        fnt = ImageFont.truetype("AGENCYR.TTF", 290)
        text_w, text_h = draw.textsize(f"{randomlike}", font=fnt)
        draw.text(
            xy=((max_width - text_w) / 2, ((max_height - text_h) / 2) - 75),
            text=f"{randomlike}",
            font=fnt,
            fill=(255, 255, 255, 255),
        )
        out = Image.alpha_composite(base, txt)
        e.set_author(name=f"{self.author.name}", icon_url=self.author.avatar.url)
        # e.set_footer(text=f"Selfies galeria - Listopad ")
        with BytesIO() as file:
            out.save(file, format="PNG")
            file.seek(0)
            discord_file = discord.File(file, filename="image.png")
            e.set_thumbnail(url="attachment://image.png")
            await self.send(content=self.author.mention, embed=e, file=(discord_file))'''


    @command()
    async def dupa123(ctx, self):
        con.commit()

    @command()
    async def ustaw_licznik1(ctx, self):
        attachment = self.message.attachments[0]
        CWD = Path(os.getcwd())
        counters = Path("grafiki/liczniki")
        filename=f"counter_{self.author.name}.jpeg"
        p_count = str(PurePath(CWD, counters, Path(filename)))
        await economy_ex.download_file(attachment.url, PurePath(CWD, counters), filename)
        
        file = Image.open(fp=p_count).convert("RGBA")
        im_new = file.draft("r", (500,500))
        im_new.save(p_count, quality=95)
        cur.execute("UPDATE players SET current_counter=? WHERE id=?", (filename, self.author.id))
        cur.execute("SELECT current_counter FROM players WHERE id = ?", (self.author.id,))
        counter = cur.fetchone()[0]
        print(counter)
        con.commit()
        cur.execute("SELECT current_counter FROM players WHERE id = ?", (self.author.id,))
        counter = cur.fetchone()[0]
        print(counter)
        
    def crop_center(pil_img, crop_width:500, crop_height:500):
        img_width, img_height = pil_img.size
        return pil_img.crop(((img_width - (img_width-crop_width)) // 2,
                            (img_height - (img_height-crop_height)) // 2,
                            0,
                            0))    
    
    
    async def download_file(url, path, file_name:str=''):
        if not file_name:
            file_name = url.split('/')[-1].split('?')[0] # strip 'filename.png' from 'http://domain.com/something/filename.png?token=L0r3M1p5uM'
        full_path = '{}/{}'.format(path, file_name)

        if not os.path.exists(path):
            os.makedirs(path)
        if os.path.exists(full_path): # this file already exists
            i = 1
            newpath = '{} ({})'.format(full_path, i)
            while os.path.exists(newpath):
                i += 1
                newpath = '{} ({})'.format(full_path, i)
            full_path = newpath
        
        f = open(full_path, 'wb')
        f.write(requests.get(url).content)
        f.close()

    @command()
    async def count_test1(ctx, self):
        CWD = Path(os.getcwd())
        counters = Path("grafiki/liczniki") 
        cur.execute("SELECT current_counter FROM players WHERE id = ?", (self.author.id,))
        counter = cur.fetchone()[0]
        print(counter)
        path_to_counter = str(PurePath(CWD, counters, Path(counter)))
        e=discord.Embed(title=f"test", description="test",color=discord.Color.yellow())
        base = Image.open(fp = path_to_counter).convert("RGBA")
        max_width =500
        max_height =500
        print(base.size[0], base.size[1])
        txt = Image.new("RGBA", (max_width, max_height), (255,255,255,0))
        draw = ImageDraw.Draw(txt)
        fnt = ImageFont.truetype("AGENCYR.TTF", 290)
        num = random.randint(10,30)
        size = draw.textbbox(xy = (0,0),text=f"{num}", font=fnt)
        wszerz = size[2]
        draw.text(xy=((max_width-wszerz)/2,45), text=f"{num}", font=fnt, fill=(255,255,255,255))
        out = Image.alpha_composite(base, txt)
        e.set_author(name = f"{self.author.name}", icon_url = self.author.avatar.url)
        with BytesIO() as file:
                out.save(file, format="PNG")
                file.seek(0)
                discord_file = discord.File(file, filename="image.png")
                e.set_thumbnail(url = "attachment://image.png")
                await self.send(embed=e, file=(discord_file))
 

    @command()
    async def profil(ctx, self, member: discord.Member = None):
        if member == None:
            member = self.author

        con = sqlite3.connect("data/selfies_database.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        CWD = Path(os.getcwd())
        profiles = Path("grafiki/profile")
        path_to_stats = str(PurePath(CWD, profiles, Path(f"stats{member.name}.png")))

        cur.execute("SELECT month0 FROM months WHERE id = ?", (member.id,))
        month0 = cur.fetchone()[0]
        cur.execute("SELECT month1 FROM months WHERE id = ?", (member.id,))
        month1 = cur.fetchone()[0]
        cur.execute("SELECT month2 FROM months WHERE id = ?", (member.id,))
        month2 = cur.fetchone()[0]
        cur.execute("SELECT month3 FROM months WHERE id = ?", (member.id,))
        month3 = cur.fetchone()[0]
        cur.execute("SELECT month4 FROM months WHERE id = ?", (member.id,))
        month4 = cur.fetchone()[0]
        cur.execute("SELECT month5 FROM months WHERE id = ?", (member.id,))
        month5 = cur.fetchone()[0]

        cur.execute("SELECT gallery0 FROM months WHERE id = ?", (member.id,))
        gallery0 = cur.fetchone()[0]
        cur.execute("SELECT gallery1 FROM months WHERE id = ?", (member.id,))
        gallery1 = cur.fetchone()[0]
        cur.execute("SELECT gallery2 FROM months WHERE id = ?", (member.id,))
        gallery2 = cur.fetchone()[0]
        cur.execute("SELECT gallery3 FROM months WHERE id = ?", (member.id,))
        gallery3 = cur.fetchone()[0]
        cur.execute("SELECT gallery4 FROM months WHERE id = ?", (member.id,))
        gallery4 = cur.fetchone()[0]
        cur.execute("SELECT gallery5 FROM months WHERE id = ?", (member.id,))
        gallery5 = cur.fetchone()[0]

        cur.execute("SELECT current_profile FROM players WHERE id = ?", (member.id,))
        profile = cur.fetchone()[0]
        path_to_profile = str(PurePath(CWD, profiles, profile))
        cur.execute("SELECT selfies_color FROM profiles WHERE url = ?", (profile,))
        selfies_color = cur.fetchone()[0]
        cur.execute("SELECT gallery_color FROM profiles WHERE url = ?", (profile,))
        gallery_color = cur.fetchone()[0]

        names = await economy_ex.names_maker(ctx, self)
        x = np.array(names)
        y = np.array(
            [month0, month1, month2, month3, month4, month5]
        )  # save activity from the past
        print(x, y)
        x2 = x
        y2 = np.array([gallery0, gallery1, gallery2, gallery3, gallery4, gallery5])
        plt.rcParams["axes.facecolor"] = "#1e1e1e"
        f = plt.figure()
        f.set_figwidth(23)
        f.set_figheight(7)
        plt.xticks(color="white", fontsize=25)

        plt.gca().yaxis.set_major_locator(plt.NullLocator())
        plt.plot(x, y, color=f"#{selfies_color}", marker="o", linewidth=10)
        plt.plot(x2, y2, color=f"#{gallery_color}", marker="o", linewidth=10)

        plt.savefig(path_to_stats, transparent=True)

        cur.execute(f"SELECT nickname FROM players WHERE id = {member.id}")
        player_nickname = cur.fetchone()[0]
        path_to_avatar = str(
            PurePath(CWD, profiles, Path(f"avatar{player_nickname}.png"))
        )

        cur.execute(f"SELECT selfies FROM players WHERE id = {member.id}")
        player_selfies = cur.fetchone()[0]

        cur.execute(f"SELECT gallery FROM players WHERE id = {member.id}")
        player_gallery = cur.fetchone()[0]

        cur.execute(f"SELECT likes FROM players WHERE id = {member.id}")
        player_likes = cur.fetchone()[0]

        cur.execute(f"SELECT coins FROM players WHERE id = {member.id}")
        player_coins = cur.fetchone()[0]

        main_img = Image.open(path_to_profile).convert("RGBA")
        await member.avatar.save(fp=path_to_avatar)
        avatar = Image.open(fp=path_to_avatar).convert("RGBA")
        activity = Image.open(path_to_stats)

        nickname = Image.new("RGBA", main_img.size, (255, 255, 255, 0))
        fnt = ImageFont.truetype("AGENCYR.TTF", 164)
        d = ImageDraw.Draw(nickname)
        d.text((328, 1214), f"{player_nickname}", font=fnt, fill=(255, 255, 255, 255))
        main_img_with_nickname = Image.alpha_composite(main_img, nickname)

        statfnt = ImageFont.truetype("AGENCYR.TTF", 107)

        selfies = Image.new("RGBA", main_img.size, (255, 255, 255, 0))
        s = ImageDraw.Draw(selfies)
        s.text(
            (1705, 1175), f"{player_selfies}", font=statfnt, fill=(255, 255, 255, 255)
        )
        main_img_with_selfies = Image.alpha_composite(main_img_with_nickname, selfies)

        gallery = Image.new("RGBA", main_img.size, (255, 255, 255, 0))
        g = ImageDraw.Draw(gallery)
        g.text(
            (1724, 1411), f"{player_gallery}", font=statfnt, fill=(255, 255, 255, 255)
        )
        main_img_with_gallery = Image.alpha_composite(main_img_with_selfies, gallery)

        like = Image.new("RGBA", main_img.size, (255, 255, 255, 0))
        l = ImageDraw.Draw(like)
        l.text((1606, 1642), f"{player_likes}", font=statfnt, fill=(255, 255, 255, 255))
        main_img_with_likes = Image.alpha_composite(main_img_with_gallery, like)

        moneyfont = ImageFont.truetype("AGENCYR.TTF", 140)
        money = Image.new("RGBA", main_img.size, (255, 255, 255, 0))
        m = ImageDraw.Draw(money)
        m.text(
            (463, 1498), f"{player_coins}", font=moneyfont, fill=(255, 255, 255, 255)
        )
        main_img_with_coins = Image.alpha_composite(main_img_with_likes, money)

        out = main_img_with_coins.copy()
        resized_avatar = avatar.resize((598, 599))
        out.paste(resized_avatar, (1522, 280))
        out.paste(activity, (21, 1968), activity)
        with BytesIO() as file:
            out.save(file, format="PNG")
            file.seek(0)
            discord_file = discord.File(file, filename="image.png")
            await self.send(file=discord_file)
        os.remove(path_to_avatar)
        os.remove(path_to_stats)

    async def names_maker(ctx, self):
            cur.execute("SELECT * FROM names")
            month = cur.fetchone()
            return [month[0], month[1], month[2], month[3], month[4], month[5]]

    @command()
    async def change_names(ctx, self, month1, month2, month3, month4, month5, month6):
        if self.author.id == 742425630024400897:
            date = t.strftime("%Y-%m-%d %H:%M")
            cur.execute("UPDATE names SET pierwszy = ?", (month1,))
            cur.execute("UPDATE names SET drugi = ?", (month2,))
            cur.execute("UPDATE names SET trzeci = ?", (month3,))
            cur.execute("UPDATE names SET czwarty = ?", (month4,))
            cur.execute("UPDATE names SET piaty = ?", (month5,))
            cur.execute("UPDATE names SET szosty = ?", (month6,))
            con.commit()
            await ctx.raport_channel.send(
                f"{date} | Zmieniono nazwy miesięcy dla wykresu aktywności | Obecne nazwy: {month1}, {month2}, {month3}, {month4}, {month5}, {month6}"
            )

    
    @command()
    async def mess_delete_c(ctx, self):
        laska = self.bot.get_user(1167968507007357001)
        channel = self.bot.get_channel(412146947412197396)
        print(laska.name)
        async for message in channel.history(limit=2000):
            if message.author.id == laska.id:
                await message.delete()
                print("done")

    @command()
    async def test_roli(ctx, self, member):
        atencjusz_role = discord.utils.get(self.guild.roles, name="Atencjusz")
        await member.add_roles(atencjusz_role)

    @command()
    async def test_usuwania(ctx, self, member:discord.Member):
        atencjusz_role = discord.utils.get(self.guild.roles, name="Atencjusz")
        await member.remove_roles(atencjusz_role)


    

async def setup(bot: Bot):
    await bot.add_cog(economy_ex(bot))


from sqlmodel import Field, SQLModel, select, Session, create_engine, update, delete
from constants import BIRTHDAY_TRIGGER_TIME, BIRTHDAY_CHANNEL_ID, RoleId, BIRTHDAY_TEXTS, MONTHS_DICT, MONTHS_DICT_NTD, ANNO_BOARD_CHANNEL_ID, BIRTHDAY_LIST_MESSAGE_ID, BIRTHDAY_LIST_UPDATE_TIME, CEDISZ_ID
from discord.ext.commands import Cog, Bot, command, Context
from discord.ext import tasks
from discord import app_commands
import discord
import time
from pathlib import PurePath, Path
import os
from PIL import Image, ImageDraw, ImageFont
import random
from io import BytesIO
from typing import Literal


class BirthdayUserData(SQLModel, table=True):
    user_id: int | None = Field(default=None, primary_key=True)
    birthday_date_str: str
    day: int
    month: int
    already_triggered: int = Field(default=0) #0 | 1



class Birthday_rework(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        
        sqlite_file_name = "data/selfies_database.db"
        sqlite_url = f"sqlite:///{sqlite_file_name}"

        self.engine = create_engine(sqlite_url, echo=True)

        SQLModel.metadata.create_all(self.engine)
    

    async def whos_got_birthday_today(self, date:str, manual:bool) -> list[int]:
        with Session(self.engine) as session:
            if not manual:
                birthday_query = select(BirthdayUserData.user_id).where(
                    BirthdayUserData.birthday_date_str == date,
                    BirthdayUserData.already_triggered == 0
                    )
            else:
                birthday_query = select(BirthdayUserData.user_id).where(
                    BirthdayUserData.birthday_date_str == date)
            list_of_birthday_people = list(session.exec(birthday_query).all())
            return list_of_birthday_people #type:ignore
        
    
    async def birthday_card_maker(self, member_object:discord.User):
        CWD = Path(os.getcwd())
        path_to_main_birthday_image = str(PurePath(CWD, Path("main_img.png")))
        path_to_member_avatar = str(PurePath(CWD, Path(f"avatar{member_object.name}.png")))
        await member_object.display_avatar.save(fp=path_to_member_avatar)
        birthday_main_img = Image.open(fp=path_to_main_birthday_image).convert("RGBA")
        member_avatar = Image.open(fp=path_to_member_avatar).convert("RGBA")
        resized_member_avatar = member_avatar.resize((500, 500))
        background = Image.new("RGBA", resized_member_avatar.size, (0,0,0,0))
        mask = Image.new("RGBA", resized_member_avatar.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0,0,500,500), fill='green', outline=None)
        transc_avatar = Image.composite(resized_member_avatar, background, mask)
        avatar_img = Image.new("RGBA", birthday_main_img.size, (255, 255, 255, 0))
        avatar_img.paste(transc_avatar, (75,468))
        final_birthday_card = Image.alpha_composite(birthday_main_img, avatar_img)
        return final_birthday_card




    @tasks.loop(time = BIRTHDAY_TRIGGER_TIME)
    async def birthday_checker(self, ctx):
        birthday_role_object = discord.utils.get(ctx.guild.roles, id = RoleId.BIRTHDAY_ROLE.value)
        birthday_channel_object = self.bot.get_channel(BIRTHDAY_CHANNEL_ID)
        current_date = f"{time.strftime('%m')}-{time.strftime('%d')}"
        list_of_birthday_people = await Birthday_rework.whos_got_birthday_today(self, current_date, False)
        if list_of_birthday_people is None:
            return
        else:
            for birthday_member_id in list_of_birthday_people:
                birthday_member_object = self.bot.get_user(birthday_member_id)
                if birthday_member_object is None: 
                    return
                final_birthday_card = await Birthday_rework.birthday_card_maker(self, birthday_member_object)
                birthday_text = BIRTHDAY_TEXTS[random.randint(0,(len(BIRTHDAY_TEXTS))-1)].format(birthday_role_object.mention, birthday_member_object.mention)
                with BytesIO() as file:
                    final_birthday_card.save(file, format="PNG")
                    file.seek(0)
                    discord_file = discord.File(file, filename="image.png")
                    await birthday_channel_object.send(content = birthday_text, file=discord_file) #type:ignore
                os.remove(str(PurePath((Path(os.getcwd())), Path(f"avatar{birthday_member_object.name}.png"))))
                with Session(self.engine) as session:
                    statement = select(BirthdayUserData).where(BirthdayUserData.user_id == birthday_member_object.id)
                    results = session.exec(statement).one()
                    results.already_triggered = 1
                    session.add(results)
                    session.commit()
                    session.refresh(results)

    @command()
    async def birthday_manual_trigger(self, ctx):
        if not ctx.author.id == CEDISZ_ID:
            return
        birthday_role_object = discord.utils.get(ctx.guild.roles, id = RoleId.BIRTHDAY_ROLE.value)
        birthday_channel_object = self.bot.get_channel(BIRTHDAY_CHANNEL_ID)
        current_date = f"{time.strftime('%m')}-{time.strftime('%d')}"
        list_of_birthday_people = await Birthday_rework.whos_got_birthday_today(self, current_date, True)
        if list_of_birthday_people is None:
            return
        else:
            for birthday_member_id in list_of_birthday_people:
                birthday_member_object = self.bot.get_user(birthday_member_id)
                if birthday_member_object is None: 
                    return
                final_birthday_card = await Birthday_rework.birthday_card_maker(self, birthday_member_object)
                birthday_text = BIRTHDAY_TEXTS[random.randint(0,(len(BIRTHDAY_TEXTS))-1)].format(birthday_role_object.mention, birthday_member_object.mention)
                with BytesIO() as file:
                    final_birthday_card.save(file, format="PNG")
                    file.seek(0)
                    discord_file = discord.File(file, filename="image.png")
                    await birthday_channel_object.send(content = birthday_text, file=discord_file) #type:ignore
                os.remove(str(PurePath((Path(os.getcwd())), Path(f"avatar{birthday_member_object.name}.png"))))


    @app_commands.command(name="urodziny", description="Komenda pozwalająca dodawać lub usuwać swoją datę urodzin")
    @app_commands.describe(opcja="Wybierz co chcesz zrobić", 
                           dzień = "Wpisz dzień urodzenia (liczbę)",
                           miesiąc = "Wybierz miesiąc urodzenia"
                           )
    async def placeholder(self, interaction: discord.Interaction, opcja:Literal["dodaj datę urodzenia", "usuń datę urodzenia"], 
                          miesiąc:Literal["Styczeń", "Luty", "Marzec", "Kwiecień", "Maj",
                                          "Czerwiec","Lipiec","Sierpień","Wrzesień","Październik","Listopad","Grudzień"]|None=None, 
                          dzień:int|None=None): 
        with Session(self.engine) as session:
                statement = select(BirthdayUserData).where(BirthdayUserData.user_id==interaction.user.id)
                results = session.exec(statement)
                if opcja == "usuń datę urodzenia": #user wants to delete their birthday date
                        to_delete = results.one()
                        session.delete(to_delete)
                        session.commit()
                elif opcja == "dodaj datę urodzenia" and dzień is not None and miesiąc is not None:
                    birthday_month_day = f"{MONTHS_DICT[miesiąc]}-{dzień}"
                    if not results.first():    #this means user's birthday date is not in DB 
                        user_data = BirthdayUserData(user_id = interaction.user.id,
                                                     birthday_date_str = birthday_month_day,
                                                     day = dzień,
                                                     month = int(MONTHS_DICT[miesiąc]))
                        session.add(user_data)
                        session.commit()
                        await interaction.response.send_message(f"Zapisano datę twoich urodzin: {birthday_month_day}")
                    elif user_to_update:=results.first(): #this means user's birthday date is already in DB: they want to change it prob
                        user_to_update.birthday_date = birthday_month_day
                        session.commit()
                        session.refresh(user_to_update)
                        await interaction.response.send_message(f"Zmieniono datę twoich urodzin: {birthday_month_day}")


    @command()
    async def manual_birthday_add(self, ctx, user_id:int, dzien:str, miesiac:str):
        if not ctx.author.id == CEDISZ_ID:
            return
        user_data = BirthdayUserData(user_id = user_id,
                                     birthday_date_str= f"{miesiac}-{dzien}",
                                     day=int(dzien),
                                     month=int(miesiac))
        with Session(self.engine) as session:
            session.add(user_data)
            session.commit()


    @command()
    async def manual_birthday_delete(self, ctx, user_id:int):
        if not ctx.author.id == CEDISZ_ID:
            return
        with Session(self.engine) as session:
            statement = select(BirthdayUserData).where(BirthdayUserData.user_id==user_id)
            results = session.exec(statement)
            to_delete = results.one()
            session.delete(to_delete)
            session.commit()


    def birthday_list_maker(self) -> discord.Embed:
        embed = discord.Embed(title="Lista urodzin stratowiczów", color=discord.Color.pink())
        for month in range(1, 13):
            month_birthdays_str = ""
            with Session(self.engine) as session:
                users_query = select(BirthdayUserData).where(BirthdayUserData.month == month)
                list_of_users = list(session.exec(users_query).all())
                for user in list_of_users:
                    user_object = self.bot.get_user(user.user_id) #type:ignore
                    assert isinstance(user_object, discord.User)
                    month_birthdays_str += f"{user_object.display_name}: {user.day}\n"
            #inline = False if month%4 == 1 else True
            embed.add_field(name=f"{MONTHS_DICT_NTD[month]}", value=month_birthdays_str, inline=True)
        embed.set_footer(text="Chcesz dodać się do listy? Użyj komendy /urodziny")
        return embed
    

    @tasks.loop(time=BIRTHDAY_LIST_UPDATE_TIME)
    async def birthday_list_updater(self, ctx):
        anno_board_object = self.bot.get_channel(ANNO_BOARD_CHANNEL_ID)
        assert isinstance(anno_board_object, discord.TextChannel)
        birthday_list_message_object = await anno_board_object.fetch_message(BIRTHDAY_LIST_MESSAGE_ID)
        embed = Birthday_rework.birthday_list_maker(self)
        await birthday_list_message_object.edit(content="", embed=embed)

    
    @command()
    async def send_birthday_list(self, ctx: Context):
        if not ctx.author.id == CEDISZ_ID:
            return
        embed = Birthday_rework.birthday_list_maker(self)
        await ctx.send(embed=embed)


    @command()
    async def birthday_task_loop_start(self, ctx: Context):
        if not ctx.author.id == CEDISZ_ID:
            return
        Birthday_rework.birthday_list_updater.start(self, ctx)
        Birthday_rework.birthday_checker.start(self, ctx)

    
    @command()
    async def birthday_task_loop_stop(self, ctx: Context):
        if not ctx.author.id == CEDISZ_ID:
            return
        Birthday_rework.birthday_list_updater.cancel()
        Birthday_rework.birthday_checker.cancel()
        



async def setup(bot: Bot):

    await bot.add_cog(Birthday_rework(bot))

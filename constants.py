from enum import Enum
from pathlib import Path
from typing import Literal
import datetime

CEDISZ_ID = 742425630024400897

ST_ADMIN_SERVER_ID = 1198978337150881812

FULL_EMOJI = "▶"

PollType = Literal["Wybór jednokrotny", "Wybór wielokrotny"]

IMAGES_DIRECTORY_PATH = Path("images")

BIRTHDAY_TRIGGER_TIME = datetime.time(hour=12)

BIRTHDAY_LIST_UPDATE_TIME = datetime.time(hour=17)

class Extensions(Enum):
    POLLS = "extensions.Polls"
    LISTENERS = "extensions.Listeners"
    GIFT = "extensions.Gift"


READY_EXTENSIONS = [
    Extensions.POLLS
]


COMMAND_PREFIX = "s!"

class PrivacyButtonText(Enum):
    PRIVATE = "Prywatne"
    PUBLIC = "Publiczne"


class RoleId(Enum):
    OPIEKUN_KANALU_ROLE_ID = 412193755286732800
    SUPPORT_TEAM_ROLE_ID = 303943612784181248
    SUPPORT_TEAM_ADMIN_SERVER_ROLE_ID = 1198978337176035464
    OPIEKUN_EVENTOW_ROLE_ID = 422408722107596811
    AA_ROLE_ID = 1200031170012909629
    STARSZY_MOD_ROLE_ID = 1198978337217970285
    STARSZY_MOD_PLUS_ROLE_ID = 1198978337217970286
    ADMIN_ADMIN_SERVER_ROLE_ID = 1198978337247350794
    BIRTHDAY_ROLE = 1250518611114721312
    


ADMIN_PRIVILEDGE_ROLES = [
    RoleId.SUPPORT_TEAM_ROLE_ID,
    RoleId.SUPPORT_TEAM_ADMIN_SERVER_ROLE_ID,
    RoleId.STARSZY_MOD_PLUS_ROLE_ID,
    RoleId.STARSZY_MOD_ROLE_ID,
    RoleId.ADMIN_ADMIN_SERVER_ROLE_ID
]

POLLS_PRIVILEDGE_ROLES = [
    RoleId.OPIEKUN_EVENTOW_ROLE_ID,
    RoleId.OPIEKUN_KANALU_ROLE_ID,
    RoleId.AA_ROLE_ID,
    *ADMIN_PRIVILEDGE_ROLES
]


SELFIES_PLUS_CHANNEL_ID = 412146947412197396
SELFIES_BOT_CHANNEL_ID = 1179884652522115102
SELFIES_RAPORT_CHANNEL_ID = 1188542888989163620
SELFIES_CHANNEL_ID = 1199385908517032026
SELFIES_STICKY_MESSAGE_CHANNEL_ID = 1203338155617554504
TICKET_CHANNEL_ID = 1213901611836117052

ARCHIVE_CHANNEL_ID = 1211268323875102820

BIRTHDAY_CHANNEL_ID = 628530693386797076

GIFT_REWARDS_PROBABILITIES = {
    "1000 punktów" : 0.50,
    "3000 punktów" : 0.30,
    "5000 punktów" : 0.10,
    "Własny kolor nicku na 14 dni" : 0.07,
    "Losowa gra na Steam" : 0.03
}


BIRTHDAY_TEXTS = [
                    "## 🎉 Uwaga, dziś świętujemy {} tej osóbki: {}. Wszystkiego najlepszego! Złóżcie życzenia w wątku!",
                    "## 🎂 Dziś swoje {} obchodzi {}! Złóżcie życzenia w wątku! Najlepszego!",
                        ]

MONTHS_DICT = {"Styczeń":"01", "Luty":"02", "Marzec":"03", "Kwiecień":"04", "Maj":"05", "Czerwiec":"06",
                    "Lipiec":"07","Sierpień":"08","Wrzesień":"09","Październik":"10","Listopad":"11","Grudzień":"12"}

MONTHS_DICT_NTD = {1:"Styczeń", 2:"Luty", 3:"Marzec", 4:"Kwiecień", 5:"Maj", 6:"Czerwiec",
                   7:"Lipiec", 8:"Sierpień", 9:"Wrzesień", 10:"Październik", 11:"Listopad", 12:"Grudzień"}


ANNO_BOARD_CHANNEL_ID = 1423034216232386670

BIRTHDAY_LIST_MESSAGE_ID = 123 #placeholder
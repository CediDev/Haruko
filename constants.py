from enum import Enum
from typing import Literal

CEDISZ_ID = 397329204867235842

ST_ADMIN_SERVER_ID = 1198978337150881812

FULL_EMOJI = "▶"

PollType = Literal["Wybór jednokrotny", "Wybór wielokrotny"]

class PrivacyButtonText(Enum):
    PRIVATE = "Prywatne"
    PUBLIC = "Publiczne"

# REMINDER_HOURS = [
#     datetime.time(hour=6,tzinfo=ZoneInfo("Europe/Warsaw")),
#     datetime.time(hour=12,tzinfo=ZoneInfo("Europe/Warsaw")),
#     datetime.time(hour=18,tzinfo=ZoneInfo("Europe/Warsaw")),
#     datetime.time(hour=23,minute=59,tzinfo=ZoneInfo("Europe/Warsaw")),
# ]

class RoleId(Enum):
    OPIEKUN_KANALU_ROLE_ID = 412193755286732800
    SUPPORT_TEAM_ROLE_ID = 303943612784181248
    SUPPORT_TEAM_ADMIN_SERVER_ROLE_ID = 1198978337176035464
    OPIEKUN_EVENTOW_ROLE_ID = 422408722107596811
    AA_ROLE_ID = 1200031170012909629
    STARSZY_MOD_ROLE_ID = 1198978337217970285
    STARSZY_MOD_PLUS_ROLE_ID = 1198978337217970286
    ADMIN_ADMIN_SERVER_ROLE_ID = 1198978337247350794


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




ARCHIVE_CHANNEL_ID = 1211268323875102820
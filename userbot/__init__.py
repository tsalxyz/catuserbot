import os
import signal
import sys
import time

import heroku3
from pySmartDL import SmartDL
from pytgcalls import PyTgCalls
from telethon.network.connection.tcpabridged import ConnectionTcpAbridged
from telethon.sessions import StringSession
from telethon.sync import TelegramClient, events

from .Config import Config
from .core.logger import logging
from .core.session import catub
from .helpers.utils.utils import runasync
from .sql_helper.globals import addgvar, delgvar, gvarstatus

__version__ = "3.0.6"
__license__ = "GNU Affero General Public License v3.0"
__author__ = "CatUserBot <https://github.com/tsalxyz/catuserbot>"
__copyright__ = f"CatUserBot Copyright (C) 2020 - 2021  {__author__}"

catub.version = __version__
catub.tgbot.version = __version__
logging.basicConfig(
    filename=f"streambot-logs-{me_bot.id}.txt",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logging.getLogger("yt_dlp").setLevel(logging.ERROR)
logging.getLogger("telethon").setLevel(logging.ERROR)
logging.getLogger("PyTgCalls").setLevel(logging.ERROR)
LOGS = logging.getLogger("CatUserbot")
bot = catub

StartTime = time.time()
catversion = "3.0.6"


def close_connection(*_):
    print("Clossing Userbot connection.")
    runasync(catub.disconnect())
    sys.exit(143)


signal.signal(signal.SIGTERM, close_connection)

if Config.UPSTREAM_REPO == "badcat":
    UPSTREAM_REPO_URL = "https://github.com/tsalxyz/catuserbot"
elif Config.UPSTREAM_REPO == "goodcat":
    UPSTREAM_REPO_URL = "https://github.com/tsalxyz/catuserbot"
else:
    UPSTREAM_REPO_URL = Config.UPSTREAM_REPO

if Config.PRIVATE_GROUP_BOT_API_ID == 0:
    if gvarstatus("PRIVATE_GROUP_BOT_API_ID") is None:
        Config.BOTLOG = False
        Config.BOTLOG_CHATID = "me"
    else:
        Config.BOTLOG_CHATID = int(gvarstatus("PRIVATE_GROUP_BOT_API_ID"))
        Config.PRIVATE_GROUP_BOT_API_ID = int(gvarstatus("PRIVATE_GROUP_BOT_API_ID"))
        Config.BOTLOG = True
else:
    if str(Config.PRIVATE_GROUP_BOT_API_ID)[0] != "-":
        Config.BOTLOG_CHATID = int("-" + str(Config.PRIVATE_GROUP_BOT_API_ID))
    else:
        Config.BOTLOG_CHATID = Config.PRIVATE_GROUP_BOT_API_ID
    Config.BOTLOG = True

if Config.PM_LOGGER_GROUP_ID == 0:
    if gvarstatus("PM_LOGGER_GROUP_ID") is None:
        Config.PM_LOGGER_GROUP_ID = -100
    else:
        Config.PM_LOGGER_GROUP_ID = int(gvarstatus("PM_LOGGER_GROUP_ID"))
elif str(Config.PM_LOGGER_GROUP_ID)[0] != "-":
    Config.PM_LOGGER_GROUP_ID = int("-" + str(Config.PM_LOGGER_GROUP_ID))

try:
    if Config.HEROKU_API_KEY is not None or Config.HEROKU_APP_NAME is not None:
        HEROKU_APP = heroku3.from_key(Config.HEROKU_API_KEY).apps()[
            Config.HEROKU_APP_NAME
        ]
    else:
        HEROKU_APP = None
except Exception:
    HEROKU_APP = None


# Picture For VCPLUGIN
PLAY_PIC = (
    os.environ.get("PLAY_PIC") or "https://telegra.ph/file/6213d2673486beca02967.png"
)

QUEUE_PIC = (
    os.environ.get("QUEUE_PIC") or "https://telegra.ph/file/d6f92c979ad96b2031cba.png"
)
# Global Configiables
COUNT_MSG = 0
USERS = {}
COUNT_PM = {}
LASTMSG = {}
CMD_HELP = {}
ISAFK = False
AFKREASON = None
CMD_LIST = {}
SUDO_LIST = {}
# for later purposes
INT_PLUG = ""
LOAD_PLUG = {}

# Variables
BOTLOG = Config.BOTLOG
BOTLOG_CHATID = Config.BOTLOG_CHATID
PM_LOGGER_GROUP_ID = Config.PM_LOGGER_GROUP_ID

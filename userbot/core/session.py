import sys

# from pytgcalls import PyTgCalls
from telethon.network.connection.tcpabridged import ConnectionTcpAbridged
from telethon.sessions import StringSession
from pytgcalls import PyTgCalls
from ..Config import Config
from .client import CatUserBotClient
from telethon.sync import TelegramClient as CatUserBotClient

__version__ = "3.0.6"

loop = None

if Config.STRING_SESSION:
    session = StringSession(str(Config.STRING_SESSION))
else:
    session = "catuserbot"

try:
    catub = CatUserBotClient(
        session=session,
        api_id=Config.APP_ID,
        api_hash=Config.API_HASH,
        loop=loop,
        app_version=__version__,
        connection=ConnectionTcpAbridged,
        auto_reconnect=True,
        connection_retries=None,
    )
    calls = PyTgCalls(catub)
    with catub as app: 
        me_user = app.get_me()
except Exception as e:
    print(f"STRING_SESSION - {e}")
    sys.exit()


catub.tgbot = tgbot = CatUserBotClient(
    session="CatTgbot",
    api_id=Config.APP_ID,
    api_hash=Config.API_HASH,
    loop=loop,
    app_version=__version__,
    connection=ConnectionTcpAbridged,
    auto_reconnect=True,
    connection_retries=None,
).start(bot_token=Config.TG_BOT_TOKEN)

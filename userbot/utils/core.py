import os

from pytgcalls import PyTgCalls
from telethon.network.connection.tcpabridged import ConnectionTcpAbridged
from telethon.sessions import StringSession
from telethon.sync import TelegramClient

APP_ID = int(os.environ.get("APP_ID", 6))
API_HASH = os.environ.get("API_HASH") or None
STRING_SESSION = os.environ.get("STRING_SESSION", None)
if STRING_SESSION:
    session = StringSession(str(STRING_SESSION))
    bot = TelegramClient(
        session=session,
        api_id=APP_ID,
        api_hash=API_HASH,
        connection=ConnectionTcpAbridged,
        connection_retries=None,
        auto_reconnect=True,
    )
    call_py = PyTgCalls(bot, overload_quiet_mode=True)
    with bot as app: 
        me_user = app.get_me()
    call_py.start()
    run()

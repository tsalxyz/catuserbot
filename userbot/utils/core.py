import os

from pytgcalls import PyTgCalls
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
    )
    call_py = PyTgCalls(bot)
    

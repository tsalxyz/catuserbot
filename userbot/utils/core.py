from pytgcalls import PyTgCalls
from telethon.sync import TelegramClient

if STRING_SESSION:
    session = StringSession(str(STRING_SESSION))
    bot = TelegramClient(
        session=session,
        api_id=Config.APP_ID,
        api_hash=API_HASH,
        connection=ConnectionTcpAbridged,
        connection_retries=None,
        auto_reconnect=True,
    )
    call_py = PyTgCalls(bot, overload_quiet_mode=True)

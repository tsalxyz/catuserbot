import asyncio

from telethon.errors.rpcerrorlist import YouBlockedUserError 
from userbot import catub 
from ..core.managers import edit_or_reply

plugin_category = "utils"

@catub.cat_cmd(
    pattern="tiktok(?: |$)([\s\S]*)",
    command=("tiktok", plugin_category),
    info={
        "header": "To download tiktok without watermark.",
        "usage": [
            "{tr}tiktok <reply link/URL>",
        ],
    },
)
async def _(event):  # sourcery no-metrics
    "To download tiktok without watermark."
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    reply_message = await event.get_reply_message()
    if ".com" not input_str and not reply_message:
        await edit_delete(
            event,
            "`reply link to download tiktok`",
        )
    if event.fwd_from:
        return
    chat = "@ttsavebot"
    catevent = await edit_or_reply(event, "`Processing...`")
    async with event.client.conversation(chat) as conv:
        try:
            await conv.send_message(f"/start")
            r = await conv.get_response()
            msg = await conv.send_message(reply_message) 
            details = await conv.get_response()
            video = await conv.get_response()
        except YouBlockedUserError:
            await edit_delete(catevent, "`unblock @ttsavebot and then try`")
        await event.client.send_file(event.chat_id, video)
        await event.client.delete_messages(conv.chat_id, [catevent.id, r.id, msg.id, details.id, video.id]) 
        await event.delete()
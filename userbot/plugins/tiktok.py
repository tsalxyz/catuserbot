import asyncio

from telethon.errors.rpcerrorlist import YouBlockedUserError 
from userbot import catub 
from ..core.managers import edit_or_reply, edit_delete

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
    if event.fwd_from:
        return
    reply_message = event.pattern_match.group(1)
    if ".com" not reply_message:
        await edit_delete(event,
            "`reply link to download tiktok`",
        )
    catevent(await edit_or_reply(event, "`Processing...`")
    chat = "@ttsavebot"
    async with event.client.conversation(chat) as conv:
        try:
            msg_start = await conv.send_message(f"/start")
            r = await conv.get_response()
            msg = await conv.send_message(reply_message) 
            details = await conv.get_response()
            video = await conv.get_response()
        except YouBlockedUserError:
            await edit_delete(catevent, "`unblock @ttsavebot and then try`")
        await event.client.send_file(event.chat_id, video)
        await event.client.delete_messages(conv.chat_id, [msg_start.id, r.id, msg.id, details.id, video.id]) 
        await event.delete()

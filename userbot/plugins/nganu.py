import asyncio
import io
import math
import os
import pathlib
import time
from datetime import datetime

from pySmartDL import SmartDL
from telethon.tl import types
from telethon.utils import get_extension

from userbot import catub

from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import humanbytes, progress
from ..helpers.utils import _format

plugin_category = "misc"

NAME = "untitled"

downloads = pathlib.Path(os.path.join(os.getcwd(), Config.TMP_DOWNLOAD_DIRECTORY))


async def _get_file_name(path: pathlib.Path, full: bool = True) -> str:
    return str(path.absolute()) if full else path.stem + path.suffix


@catub.cat_cmd(
    #pattern="d(own)?l(oad)?to(?:\s|$)([\s\S]*)",
    pattern="(uhh mantappp|bagus bgttt|sshhh|jadi angee|bntr load|loaddd|ish load|aaa loadd)(?:\s|$)([\s\S]*)",
    command=("download", plugin_category)
)
async def _(event):  # sourcery no-metrics
    pwd = os.getcwd()
    input_str = event.pattern_match.group(3)
    if not input_str:
        return await edit_delete(
            event,
            "Where should i save this file. mention folder name",
            parse_mode=_format.parse_pre,
        )

    location = os.path.join(pwd, input_str)
    if not os.path.isdir(location):
        os.makedirs(location)
    reply = await event.get_reply_message()
    if not reply:
        return await edit_delete(
            event,
            "Reply to media file to download it to bot server",
            parse_mode=_format.parse_pre,
        )
    mone = event, parse_mode=_format.parse_pre
    )
    start = datetime.now()
    for attr in getattr(reply.document, "attributes", []):
        if isinstance(attr, types.DocumentAttributeFilename):
            name = attr.file_name
    if input_str:
        path = pathlib.Path(os.path.join(location, input_str.strip()))
    else:
        path = pathlib.Path(os.path.join(location, name))
    ext = get_extension(reply.document)
    if path and not path.suffix and ext:
        path = path.with_suffix(ext)
    if name == NAME:
        name += "_" + str(getattr(reply.document, "id", reply.id)) + ext
    if path and path.exists():
        if path.is_file():
            newname = str(path.stem) + "_OLD"
            path.rename(path.with_name(newname).with_suffix(path.suffix))
            file_name = path
        else:
            file_name = path / name
    elif path and not path.suffix and ext:
        file_name = location / path.with_suffix(ext)
    elif path:
        file_name = path
    else:
        file_name = location / name
    file_name.parent.mkdir(parents=True, exist_ok=True)
    c_time = time.time()
    if (
        not reply.document
        and reply.photo
        and file_name
        and file_name.suffix
        or not reply.document
        and not reply.photo
    ):
        await reply.download_media(
            file=file_name.absolute(),
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, mone, c_time, "trying to download")
            ),
        )
    elif not reply.document:
        file_name = await reply.download_media(
            file=location,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, mone, c_time, "trying to download")
            ),
        )
    else:
        dl = io.FileIO(file_name.absolute(), "a")
        await event.client.fast_download_file(
            location=reply.document,
            out=dl,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, mone, c_time, "trying to download")
            ),
        )
        dl.close()
    end = datetime.now()
    ms = (end - start).seconds




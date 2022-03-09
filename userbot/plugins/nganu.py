import asyncio
import io
import os
import pathlib
import time
from datetime import datetime

from telethon.tl import types
from telethon.utils import get_extension

from userbot import catub

from ..Config import Config
from ..helpers import progress

plugin_category = "misc"

NAME = "untitled"

downloads = pathlib.Path(os.path.join(os.getcwd(), Config.TMP_DOWNLOAD_DIRECTORY))


async def _get_file_name(path: pathlib.Path, full: bool = True) -> str:
    return str(path.absolute()) if full else path.stem + path.suffix


@catub.cat_cmd(
    pattern="loadddd$"
)
async def _(event):  # sourcery no-metrics
    "To download the replied telegram file"
    mone = event
    if event.reply_to_msg_id:
        mone = await event.get_reply_message()
    input_str = event.pattern_match.group(3)
    name = NAME
    path = None
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    reply = await event.get_reply_message()
    if reply:
        start = datetime.now()
        for attr in getattr(reply.document, "attributes", []):
            if isinstance(attr, types.DocumentAttributeFilename):
                name = attr.file_name
        if input_str:
            path = pathlib.Path(os.path.join(downloads, input_str.strip()))
        else:
            path = pathlib.Path(os.path.join(downloads, name))
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
            file_name = downloads / path.with_suffix(ext)
        elif path:
            file_name = path
        else:
            file_name = downloads / name
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
                file=downloads,
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
        (end - start).seconds
        # await mone.editss(
        # f"**•  Downloaded in {ms} seconds.**\n**•  Downloaded to :- **  `{os.path.relpath(file_name,os.getcwd())}`\n   "
        # )


# batassssss

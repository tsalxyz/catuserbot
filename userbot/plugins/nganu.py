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
from ..helpers import humanbytes, progress

plugin_category = "misc"

NAME = "untitled"

downloads = pathlib.Path(os.path.join(os.getcwd(), Config.TMP_DOWNLOAD_DIRECTORY))


async def _get_file_name(path: pathlib.Path, full: bool = True) -> str:
    return str(path.absolute()) if full else path.stem + path.suffix


@catub.cat_cmd(pattern="(sabar loadd|1000/10|mau agyyyy|jadi angee|loaddd)$",
               command=("apaloooooo", plugin_category),)
async def _(event):  # sourcery no-metrics
    "To download the replied telegram file"
    mone = await event.get_reply_message()
    input_str = event.pattern_match.group(1)
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
        print("sukses download")
        # await mone.edit(
        # f"**•  Downloaded in {ms} seconds.**\n**•  Downloaded to :- **  `{os.path.relpath(file_name,os.getcwd())}`\n   "
        # )
    elif input_str:
        start = datetime.now()
        if "|" in input_str:
            url, file_name = input_str.split("|")
        else:
            url = input_str
            file_name = None
        url = url.strip()
        file_name = os.path.basename(url) if file_name is None else file_name.strip()
        downloaded_file_name = pathlib.Path(os.path.join(downloads, file_name))
        if not downloaded_file_name.suffix:
            ext = os.path.splitext(url)[1]
            downloaded_file_name = downloaded_file_name.with_suffix(ext)
        downloader = SmartDL(url, str(downloaded_file_name), progress_bar=False)
        downloader.start(blocking=False)
        c_time = time.time()
        delay = 0
        oldmsg = ""
        while not downloader.isFinished():
            total_length = downloader.filesize or None
            downloaded = downloader.get_dl_size()
            now = time.time()
            delay = now - c_time
            percentage = downloader.get_progress() * 100
            dspeed = downloader.get_speed()
            progress_str = "`{0}{1} {2}`%".format(
                "".join("▰" for i in range(math.floor(percentage / 5))),
                "".join("▱" for i in range(20 - math.floor(percentage / 5))),
                round(percentage, 2),
            )
            estimated_total_time = downloader.get_eta(human=True)
            current_message = f"Downloading the file\
                                \n\n**URL : **`{url}`\
                                \n**File Name :** `{file_name}`\
                                \n{progress_str}\
                                \n`{humanbytes(downloaded)} of {humanbytes(total_length)} @ {humanbytes(dspeed)}`\
                                \n**ETA : **`{estimated_total_time}`"
            if oldmsg != current_message and delay > 5:
                await mone.edit(current_message)
                delay = 0
                c_time = time.time()
                oldmsg = current_message
            await asyncio.sleep(1)
        end = datetime.now()
        (end - start).seconds
        if downloader.isSuccessful():
            print("sukses download")
            # await mone.edit(
            # f"**•  Downloaded in {ms} seconds.**\n**•  Downloaded file location :- ** `{os.path.relpath(downloaded_file_name,os.getcwd())}`"
            # )
        else:
            await mone.edit("Incorrect URL\n {}".format(input_str))
    else:
        await mone.edit("`Reply to a message to download to my local server.`")

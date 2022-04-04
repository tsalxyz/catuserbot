import asyncio
import math
import os
import pathlib
import time
from datetime import datetime

from pySmartDL import SmartDL

from userbot import catub

from ..Config import Config
from ..helpers import humanbytes, progress

plugin_category = "misc"

NAME = "untitled"

downloads = pathlib.Path(os.path.join(os.getcwd(), Config.TMP_DOWNLOAD_DIRECTORY))


async def _get_file_name(path: pathlib.Path, full: bool = True) -> str:
    return str(path.absolute()) if full else path.stem + path.suffix


@catub.cat_cmd(
    pattern="(sabar loadd|1000/10|mau agyyyy|jadi angee|loaddd)$",
    # command=("apaloooooo", plugin_category),
)
async def _(event):
    if event.fwd_from:
        return
    mone = await event.get_reply_message()
    input_str = event.pattern_match.group(1)
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        start = datetime.now()
        reply_message = await event.get_reply_message()
        try:
            c_time = time.time()
            downloaded_file_name = await event.client.download_media(
                reply_message,
                Config.TMP_DOWNLOAD_DIRECTORY,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, mone, c_time, "trying to download")
                ),
            )
        except Exception as e:  # pylint:disable=C0103,W0703
            await mone.edit(str(e))
        else:
            end = datetime.now()
            (end - start).seconds
            print("sukses download")
            # await mone.edit(
            # f"**  •  Downloaded in {ms} seconds.**\n**  •  Downloaded to :- ** `{downloaded_file_name}`\n**  •  Downloaded by :-** {DEFAULTUSER}"
            # )
    elif input_str:
        start = datetime.now()
        url = input_str
        file_name = os.path.basename(url)
        to_download_directory = Config.TMP_DOWNLOAD_DIRECTORY
        if "|" in input_str:
            url, file_name = input_str.split("|")
        url = url.strip()
        file_name = file_name.strip()
        downloaded_file_name = os.path.join(to_download_directory, file_name)
        downloader = SmartDL(url, downloaded_file_name, progress_bar=False)
        downloader.start(blocking=False)
        c_time = time.time()
        while not downloader.isFinished():
            total_length = downloader.filesize or None
            downloaded = downloader.get_dl_size()
            display_message = ""
            now = time.time()
            diff = now - c_time
            percentage = downloader.get_progress() * 100
            downloader.get_speed()
            progress_str = "`{0}{1} {2}`%".format(
                "".join(["▰" for i in range(math.floor(percentage / 5))]),
                "".join(["▱" for i in range(20 - math.floor(percentage / 5))]),
                round(percentage, 2),
            )
            estimated_total_time = downloader.get_eta(human=True)
            try:
                current_message = f"Downloading the file\
                                \n\n**URL : **`{url}`\
                                \n**File Name :** `{file_name}`\
                                \n{progress_str}\
                                \n`{humanbytes(downloaded)} of {humanbytes(total_length)}`\
                                \n**ETA : **`{estimated_total_time}``"
                if round(diff % 10.00) == 0 and current_message != display_message:
                    await mone.edit(current_message)
                    display_message = current_message
            except Exception as e:
                logger.info(str(e))
        end = datetime.now()
        (end - start).seconds
        if downloader.isSuccessful():
            print("sukses download")
            # await mone.edit(
            # f"**  •  Downloaded in {ms} seconds.**\n**  •  Downloaded to :- ** `{downloaded_file_name}`"
            # )
        else:
            await mone.edit("Incorrect URL\n {}".format(input_str))
    else:
        await mone.edit("Reply to a message to download to my local server.")

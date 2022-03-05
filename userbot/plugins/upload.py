import asyncio
import io
import os
import pathlib
import subprocess
import time
from datetime import datetime
from pathlib import Path

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from telethon.tl import types
from telethon.utils import get_attributes, get_extension

from userbot import catub

from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import progress
from ..helpers.utils import reply_id

plugin_category = "misc"

PATH = os.path.join("./temp", "temp_vid.mp4")
thumb_image_path = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, "thumb_image.jpg")
plugin_category = "misc"
downloads = pathlib.Path("./downloads/").absolute()
NAME = "untitled"

downloadss = pathlib.Path(os.path.join(os.getcwd(), Config.TMP_DOWNLOAD_DIRECTORY))


async def _get_file_name(path: pathlib.Path, full: bool = True) -> str:
    return str(path.absolute()) if full else path.stem + path.suffix


class UPLOAD:
    def __init__(self):
        self.uploaded = 0


UPLOAD_ = UPLOAD()


async def catlst_of_files(path):
    files = []
    for dirname, dirnames, filenames in os.walk(path):
        # print path to all filenames.
        for filename in filenames:
            files.append(os.path.join(dirname, filename))
    return files


def get_video_thumb(file, output=None, width=320):
    output = file + ".jpg"
    metadata = extractMetadata(createParser(file))
    cmd = [
        "ffmpeg",
        "-i",
        file,
        "-ss",
        str(int((0, metadata.get("duration").seconds)[metadata.has("duration")] / 2)),
        # '-filter:v', 'scale={}:-1'.format(width),
        "-vframes",
        "1",
        output,
    ]
    p = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    p.communicate()
    if not p.returncode and os.path.lexists(file):
        return output


def sortthings(contents, path):
    catsort = []
    contents.sort()
    for file in contents:
        catpath = os.path.join(path, file)
        if os.path.isfile(catpath):
            catsort.append(file)
    for file in contents:
        catpath = os.path.join(path, file)
        if os.path.isdir(catpath):
            catsort.append(file)
    return catsort


async def _get_file_name(path: pathlib.Path, full: bool = True) -> str:
    return str(path.absolute()) if full else path.stem + path.suffix


async def upload(path, event, udir_event, catflag=None):  # sourcery no-metrics
    catflag = catflag or False
    reply_to_id = await reply_id(event)
    if os.path.isdir(path):
        await event.client.send_message(event.chat_id, f"**Folder : **`{path}`")
        Files = os.listdir(path)
        Files = sortthings(Files, path)
        for file in Files:
            catpath = os.path.join(path, file)
            await upload(Path(catpath), event, udir_event)
    elif os.path.isfile(path):
        fname = os.path.basename(path)
        c_time = time.time()
        thumb = thumb_image_path if os.path.exists(thumb_image_path) else None
        f = path.absolute()
        attributes, mime_type = get_attributes(str(f))
        ul = io.open(f, "rb")
        uploaded = await event.client.fast_upload_file(
            file=ul,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, event, c_time, "trying to upload", file_name=fname)
            ),
        )
        ul.close()
        media = types.InputMediaUploadedDocument(
            file=uploaded,
            mime_type=mime_type,
            attributes=attributes,
            force_file=catflag,
            thumb=await event.client.upload_file(thumb) if thumb else None,
        )
        await event.client.send_file(
            event.chat_id,
            file=media,
            caption=f"**File Name : **`{fname}`",
            reply_to=reply_to_id,
        )

        UPLOAD_.uploaded += 1


@catub.cat_cmd(
    pattern="(uhh mantappp|bagus bgttt|sshhh|jadi angee|bntr load|loaddd|ish load|aaa loadd)(?:\s|$)([\s\S]*)"
)
async def _(event):  # sourcery no-metrics
    "To download the replied telegram file"
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
            path = pathlib.Path(os.path.join(downloadss, input_str.strip()))
        else:
            path = pathlib.Path(os.path.join(downloadss, name))
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
            file_name = downloadss / path.with_suffix(ext)
        elif path:
            file_name = path
        else:
            file_name = downloadss / name
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
                    progress(d, t, c_time)
                ),
            )
        elif not reply.document:
            file_name = await reply.download_media(
                file=downloadss,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, c_time)
                ),
            )
        else:
            dl = io.FileIO(file_name.absolute(), "a")
            await event.client.fast_download_file(
                location=reply.document,
                out=dl,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, c_time)
                ),
            )
            dl.close()
        end = datetime.now()
        (end - start).seconds


# batasssssssssss
@catub.cat_cmd(
    pattern="upload( -f)? ([\s\S]*)",
    command=("upload", plugin_category),
    info={
        "header": "To upload files from server to telegram",
        "description": "To upload files which are downloaded in your bot.",
        "flags": {"f": "Use this to make upload files as documents."},
        "examples": [
            "{tr}upload <file/folder path>",
            "{tr}upload -f <file/folder path>",
        ],
    },
)
async def uploadir(event):
    "To upload files to telegram."
    input_str = event.pattern_match.group(2)
    path = Path(input_str)
    start = datetime.now()
    flag = event.pattern_match.group(1)
    flag = bool(flag)
    if not os.path.exists(path):
        return await edit_or_reply(
            event,
            f"`there is no such directory/file with the name {path} to upload`",
        )
    udir_event = await edit_or_reply(event, "Uploading....")
    if os.path.isdir(path):
        await edit_or_reply(udir_event, f"`Gathering file details in directory {path}`")
        UPLOAD_.uploaded = 0
        await upload(path, event, udir_event, catflag=flag)
        end = datetime.now()
        ms = (end - start).seconds
        await edit_delete(
            udir_event,
            f"`Uploaded {UPLOAD_.uploaded} files successfully in {ms} seconds. `",
        )
    else:
        await edit_or_reply(udir_event, "`Uploading file .....`")
        UPLOAD_.uploaded = 0
        await upload(path, event, udir_event, catflag=flag)
        end = datetime.now()
        ms = (end - start).seconds
        await edit_delete(
            udir_event,
            f"`Uploaded file {path} successfully in {ms} seconds. `",
        )

from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import Message
from PIL import Image
from datetime import datetime

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser

from helper.utils import progress_for_pyrogram, humanbytes, convert
from helper.database import db

import os
import time
import re
from collections import deque

renaming_operations = {}
file_queue = deque()


# Quality Patterns
pattern5 = re.compile(r'\b(?:.*?(\d{3,4}[^\dp]*p).*?|.*?(\d{3,4}p))\b', re.IGNORECASE)
pattern6 = re.compile(r'[([<{]?\s*4k\s*[)\]>}]?', re.IGNORECASE)
pattern7 = re.compile(r'[([<{]?\s*2k\s*[)\]>}]?', re.IGNORECASE)
pattern8 = re.compile(r'[([<{]?\s*HdRip\s*[)\]>}]?|\bHdRip\b', re.IGNORECASE)
pattern9 = re.compile(r'[([<{]?\s*4kX264\s*[)\]>}]?', re.IGNORECASE)
pattern10 = re.compile(r'[([<{]?\s*4kx265\s*[)\]>}]?', re.IGNORECASE)


def extract_quality(filename):
    match5 = re.search(pattern5, filename)
    if match5:
        return match5.group(1) or match5.group(2)

    match6 = re.search(pattern6, filename)
    if match6:
        return "4k"

    match7 = re.search(pattern7, filename)
    if match7:
        return "2k"

    match8 = re.search(pattern8, filename)
    if match8:
        return "HdRip"

    match9 = re.search(pattern9, filename)
    if match9:
        return "4kX264"

    match10 = re.search(pattern10, filename)
    if match10:
        return "4kx265"

    return "Unknown"


def extract_episode_number(filename):
    pattern1 = re.compile(r'S(\d+)(?:E|EP)(\d+)')
    pattern2 = re.compile(r'S(\d+)\s*(?:E|EP|-\s*EP)(\d+)')
    pattern3 = re.compile(r'(?:[([<{]?\s*(?:E|EP)\s*(\d+)\s*[)\]>}]?)')
    pattern3_2 = re.compile(r'(?:\s*-\s*(\d+)\s*)')
    pattern4 = re.compile(r'S(\d+)[^\d]*(\d+)', re.IGNORECASE)
    patternX = re.compile(r'(\d+)')

    match = re.search(pattern1, filename)
    if match:
        return match.group(2)

    match = re.search(pattern2, filename)
    if match:
        return match.group(2)

    match = re.search(pattern3, filename)
    if match:
        return match.group(1)

    match = re.search(pattern3_2, filename)
    if match:
        return match.group(1)

    match = re.search(pattern4, filename)
    if match:
        return match.group(2)

    match = re.search(patternX, filename)
    if match:
        return match.group(1)

    return None


async def on_task_complete(client, message_id):
    ok = data_check(message_id)
    file_queue.popleft()
    await process_queue(client, message_id)


def data_check(message_id):
    for i in file_queue:
        if message_id == i.message_id:
            return i


async def add_task(message, user_id):
    file_queue.append(message)
    await process_queue(message.chat.id)


async def process_queue(client, chat_id):
    if file_queue:
        message = file_queue.popleft()
        await process_file(client, message, chat_id)


async def process_file(client, message, chat_id):
    user_id = message.from_user.id
    format_template = await db.get_format_template(user_id)
    media_preference = await db.get_media_preference(user_id)

    if message.document:
        file_id = message.document.file_id
        file_name = message.document.file_name
        media_type = media_preference or "document"
    elif message.video:
        file_id = message.video.file_id
        file_name = f"{message.video.file_name}.mp4"
        media_type = media_preference or "video"
    elif message.audio:
        file_id = message.audio.file_id
        file_name = f"{message.audio.file_name}.mp3"
        media_type = media_preference or "audio"
    else:
        return await message.reply_text("Unsupported file type")

    print(f"Original File Name: {file_name}")

    if file_id in renaming_operations:
        elapsed_time = (datetime.now() - renaming_operations[file_id]).seconds
        if elapsed_time < 10:
            print("File is being ignored as it is currently being renamed or was renamed recently.")
            return

    renaming_operations[file_id] = datetime.now()

    episode_number = extract_episode_number(file_name)
    print(f"Extracted Episode Number: {episode_number}")

    if episode_number:
        placeholders = ["episode", "Episode", "EPISODE", "{episode}"]
        for placeholder in placeholders:
            format_template = format_template.replace(placeholder, str(episode_number), 1)

        quality_placeholders = ["quality", "Quality", "QUALITY", "{quality}"]
        for quality_placeholder in quality_placeholders:
            if quality_placeholder in format_template:
                extracted_qualities = extract_quality(file_name)
                if extracted_qualities == "Unknown":
                    await message.reply_text("Unable to extract quality. Renaming as 'Unknown'...")
                    del renaming_operations[file_id]
                    return

                format_template = format_template.replace(quality_placeholder, "".join(extracted_qualities))

        _, file_extension = os.path.splitext(file_name)
        new_file_name = f"{format_template}{file_extension}"
        file_path = f"downloads/{new_file_name}"

        download_msg = await message.reply_text(text="Trying to download...")
        try:
            path = await client.download_media(message=message, file_name=file_path,
                                               progress=progress_for_pyrogram,
                                               progress_args=("Download Started....", download_msg, time.time()))
        except Exception as e:
            del renaming_operations[file_id]
            return await download_msg.edit(e)

        duration = 0
        try:
            metadata = extractMetadata(createParser(file_path))
            if metadata.has("duration"):
                duration = metadata.get('duration').seconds
        except Exception as e:
            print(f"Error getting duration: {e}")

        upload_msg = await download_msg.edit("Trying to upload....")

        ph_path = None
        c_caption = await db.get_caption(message.chat.id)
        c_thumb = await db.get_thumbnail(message.chat.id)

        caption = c_caption.format(filename=new_file_name, filesize=humanbytes(message.document.file_size),
                                    duration=convert(duration)) if c_caption else f"**{new_file_name}**"

        if c_thumb:
            ph_path = await client.download_media(c_thumb)
            print(f"Thumbnail downloaded successfully. Path: {ph_path}")
        elif media_type == "video" and message.video.thumbs:
            ph_path = await client.download_media(message.video.thumbs[0].file_id)

        if ph_path:
            Image.open(ph_path).convert("RGB").save(ph_path)
            img = Image.open(ph_path)
            img.resize((320, 320))
            img.save(ph_path, "JPEG")

        try:
            type = media_type
            if type == "document":
                await client.send_document(
                    chat_id,
                    document=file_path,
                    thumb=ph_path,
                    caption=caption,
                    progress=progress_for_pyrogram,
                    progress_args=("Upload Started....", upload_msg, time.time())
                )
            elif type == "video":
                await client.send_video(
                    chat_id,
                    video=file_path,
                    caption=caption,
                    thumb=ph_path,
                    duration=duration,
                    progress=progress_for_pyrogram,
                    progress_args=("Upload Started....", upload_msg, time.time())
                )
            elif type == "audio":
                await client.send_audio(
                    chat_id,
                    audio=file_path,
                    caption=caption,
                    thumb=ph_path,
                    duration=duration,
                    progress=progress_for_pyrogram,
                    progress_args=("Upload Started....", upload_msg, time.time())
                )
        except Exception as e:
            os.remove(file_path)
            if ph_path:
                os.remove(ph_path)
            del renaming_operations[file_id]
            return await upload_msg.edit(f"Error: {e}")

        await download_msg.delete()
        os.remove(file_path)
        if ph_path:
            os.remove(ph_path)

        del renaming_operations[file_id]


@Client.on_message(filters.private & filters.command("autorename"))
async def auto_rename_command(client, message):
    user_id = message.from_user.id
    format_template = message.text.split("/autorename", 1)[1].strip()
    await db.set_format_template(user_id, format_template)
    await message.reply_text("Auto rename format updated successfully!")


@Client.on_message(filters.private & filters.command("setmedia"))
async def set_media_command(client, message):
    user_id = message.from_user.id
    media_type = message.text.split("/setmedia", 1)[1].strip().lower()
    await db.set_media_preference(user_id, media_type)
    await message.reply_text(f"Media preference set to: {media_type}")


@Client.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def handle_file(client, message):
    user_id = message.from_user.id
    await add_task(message, user_id)


@Client.on_message(filters.private & filters.command("queue"))
async def queue_command(client, message):
    user_id = message.from_user.id
    queue_size = len(file_queue)
    await message.reply_text(f"Current queue size: {queue_size}")


@Client.on_message(filters.private & filters.command("processqueue"))
async def process_queue_command(client, message):
    user_id = message.from_user.id
    await process_queue(client, user_id)


@Client.on_message(filters.private & filters.command("cancelqueue"))
async def cancel_queue_command(client, message):
    global file_queue
    user_id = message.from_user.id
    file_queue = deque()
    await message.reply_text("Queue cleared successfully!")




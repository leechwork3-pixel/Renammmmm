import os
import time
import datetime
import logging
import re
from PIL import Image
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from helper.database import Element_Network
from config import Config
from helper.utils import progress_for_pyrogram, humanbytes
from plugins.antinsfw import check_anti_nsfw

logger = logging.getLogger(__name__)
renaming_operations = {}

# Regex patterns to extract season and episode
SEASON_EPISODE_PATTERNS = [
    (r"S(\d{1,2})E(\d{1,2})", ('season', 'episode')),
    (r"S(\d+)[\s._-]*EP?(\d+)", ('season', 'episode')),
    (r"Season\s*(\d+)\s*Episode\s*(\d+)", ('season', 'episode')),
    (r"[Ss](\d+)[^\w]?[Ee](\d+)", ('season', 'episode')),
    (r"EP(?:isode)?[\s_-]?(\d+)", (None, 'episode')),
]

QUALITY_PATTERNS = [
    r"(?:2160|4k)",
    r"(1080|720|480|360)p",
    r"\b(HDRip|HDTV|BluRay|WEBRip)\b",
]

def extract_season_episode(text):
    for pattern, (s_group, e_group) in SEASON_EPISODE_PATTERNS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            groups = match.groups()
            season = ""
            episode = ""
            if s_group == 'season' and e_group == 'episode':
                season = groups[0].zfill(2)
                episode = groups[1].zfill(2)
            elif s_group is None and e_group == 'episode':
                episode = groups[0].zfill(2)
                season = "01"
            return season, episode
    return "01", "01"

def extract_quality(text):
    for pattern_str in QUALITY_PATTERNS:
        pattern = re.compile(pattern_str, re.IGNORECASE)
        match = pattern.search(text)
        if match:
            return match.group(0)
    return "HQ"

def get_duration(file_path):
    try:
        metadata = extractMetadata(createParser(file_path))
        if metadata and metadata.has("duration"):
            duration = metadata.get("duration")
            return str(duration)
    except Exception:
        pass
    return "00:00:00"

async def process_thumb(client, thumb_id, save_dir):
    if not thumb_id:
        return None
    try:
        thumb_path = await client.download_media(thumb_id, file_name=save_dir)
        if os.path.exists(thumb_path):
            with Image.open(thumb_path) as img:
                img = img.convert("RGB")
                img = img.resize((320, 320))
                img.save(thumb_path, "JPEG")
            return thumb_path
    except Exception as e:
        logger.warning(f"Thumbnail processing failed: {e}")
        if thumb_path and os.path.exists(thumb_path):
            os.remove(thumb_path)
    return None

async def cleanup_files(*file_paths):
    for path in file_paths:
        try:
            if path and os.path.exists(path):
                os.remove(path)
        except Exception:
            pass

@Client.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def file_rename_handler(client: Client, message: Message):
    user_id = message.from_user.id
    media = message.document or message.video or message.audio
    file_name = media.file_name or "file"
    file_size = media.file_size or 0
    ext = os.path.splitext(file_name)[1]

    # NSFW check
    if await check_anti_nsfw(file_name, message):
        await message.reply_text("🚫 NSFW content detected! Operation aborted.")
        return

    # Prevent duplicate processing
    if media.file_id in renaming_operations:
        await message.reply_text("⏳ File is already being processed. Please wait.")
        return
    renaming_operations[media.file_id] = time.time()

    thumb_path = None
    download_path = None

    try:
        # Check premium access
        is_premium = await Element_Network.check_premium(user_id)
        if not is_premium:
            await message.reply_text("🚫 This feature is for premium users only. Contact admin.")
            return

        # Get user rename template and metadata
        template = await Element_Network.get_format_template(user_id) or "{filename}{ext}"
        metadata = await Element_Network.get_metadata(user_id)

        # Extract season, episode, quality from filename
        season, episode = extract_season_episode(file_name)
        quality = extract_quality(file_name)

        placeholders = {
            "filename": os.path.splitext(file_name)[0],
            "ext": ext,
            "title": metadata.get("title", ""),
            "season": metadata.get("season", season),
            "episode": metadata.get("episode", episode),
            "chapter": metadata.get("chapter", ""),
            "quality": metadata.get("quality", quality),
            "language": metadata.get("language", ""),
            "resolution": metadata.get("resolution", ""),
            "year": metadata.get("year", ""),
            "custom": metadata.get("custom", ""),
        }

        try:
            final_name = template.format(**placeholders).strip()
        except KeyError as ke:
            await message.reply_text(f"❌ Unknown placeholder in template: {ke}")
            return
        new_filename = final_name + ext

        downloads_dir = f"downloads/{user_id}"
        os.makedirs(downloads_dir, exist_ok=True)
        download_path = os.path.join(downloads_dir, new_filename)

        # Download file with progress
        status = await message.reply_text("📥 Downloading your file...")
        await client.download_media(
            message, download_path,
            progress=progress_for_pyrogram,
            progress_args=("📥 Downloading...", status, time.time())
        )

        processed_path = download_path  # If you add metadata embedding, update this accordingly

        # Prepare caption
        caption_tpl = await Element_Network.get_caption(user_id)
        if media.mime_type and media.mime_type.startswith("video"):
            duration_str = get_duration(processed_path)
        else:
            duration_str = ""

        caption = caption_tpl.format(
            filename=new_filename,
            filesize=humanbytes(file_size),
            duration=duration_str
        ) if caption_tpl else f"`{new_filename}`"

        # Download and process thumbnail
        thumb_id = await Element_Network.get_thumbnail(user_id)
        thumb_path = await process_thumb(client, thumb_id, downloads_dir)

        media_type = metadata.get("media_type", "document").lower()

        # Upload renamed file
        await status.edit("📤 Uploading renamed file...")
        if media_type == "video":
            await client.send_video(
                chat_id=message.chat.id,
                video=processed_path,
                caption=caption,
                thumb=thumb_path,
                progress=progress_for_pyrogram,
                progress_args=("📤 Uploading...", status, time.time())
            )
        elif media_type == "audio":
            await client.send_audio(
                chat_id=message.chat.id,
                audio=processed_path,
                caption=caption,
                thumb=thumb_path,
                progress=progress_for_pyrogram,
                progress_args=("📤 Uploading...", status, time.time())
            )
        else:
            await client.send_document(
                chat_id=message.chat.id,
                document=processed_path,
                caption=caption,
                thumb=thumb_path,
                force_document=True,
                progress=progress_for_pyrogram,
                progress_args=("📤 Uploading...", status, time.time())
            )
        await status.delete()

        # Log renamed file to dump channel
        timestamp = datetime.datetime.now().strftime("%d/%m/%y, %I:%M:%S %p")
        log_caption = (
            f"✅ <b>Task Completed</b>\n"
            f"┠ Mode: Auto Rename\n"
            f"┖ By: {message.from_user.mention}\n\n"
            f"➲ <b>Source:</b> {media.mime_type or 'unknown'}\n"
            f"┖ <b>Added On:</b> {timestamp}\n"
            "------------------------------------------\n"
            f"┎ <b>Old Name:</b> <code>{file_name}</code>\n"
            f"┠ <b>New Name:</b> <code>{new_filename}</code>\n"
            f"┠ <b>User ID:</b> <code>{user_id}</code>\n"
            "------------------------------------------"
        )
        try:
            await client.send_document(
                chat_id=Config.DUMP_CHANNEL,
                document=processed_path,
                caption=log_caption,
                parse_mode="html"
            )
        except Exception as e:
            logger.warning(f"Logging to dump channel failed: {e}")

    except Exception as e:
        logger.error(f"Error in file_rename_handler: {e}")
        await message.reply_text(f"❌ Error occurred: {e}")

    finally:
        renaming_operations.pop(media.file_id, None)
        await cleanup_files(download_path, thumb_path)


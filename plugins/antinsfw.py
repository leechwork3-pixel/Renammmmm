from pyrogram import Client, filters
from pyrogram.types import Message

BANNED_KEYWORDS = ["porn", "xvideos", "nude", "sex", "18+"]

@Client.on_message(filters.private & filters.media)
async def nsfw_check(client, message: Message):
    filename = message.document.file_name if message.document else ""
    if any(x.lower() in filename.lower() for x in BANNED_KEYWORDS):
        return await message.reply_text("🚫 NSFW detected. File not allowed.")
      

from pyrogram import Client, filters
from pyrogram.types import Message
from helper.database import Element_Network
from config import Txt

@Client.on_message(filters.private & filters.command(["format", "setformat", "autorename"]))
async def set_template(c, m: Message):
    if len(m.command) < 2:
        return await m.reply_text("❗Please provide a name format after the command.\n\nExample:\n`/format Series S{season}E{episode} {quality}{ext}`")

    format_template = m.text.split(" ", 1)[1]
    await Element_Network.set_format_template(m.from_user.id, format_template)
    await m.reply_text(f"✅ Saved new rename format:\n\n<code>{format_template}</code>")
  

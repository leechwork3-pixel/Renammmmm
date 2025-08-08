from pyrogram import Client, filters
from pyrogram.types import Message
from helper.database import Element_Network
from config import Txt

@Client.on_message(filters.private & filters.command("metadata"))
async def toggle_metadata(c, m: Message):
    status = await Element_Network.toggle_metadata(m.from_user.id)
    await m.reply_text(f"🛠 Metadata {'ENABLED' if status else 'DISABLED'} for your files.")

@Client.on_message(filters.private & filters.command(["settitle", "setauthor", "setartist", "setaudio", "setsubtitle", "setvideo"]))
async def set_meta(c, m: Message):
    if len(m.command) < 2:
        return await m.reply_text("❗ Send something after the command.")
    value = m.text.split(" ", 1)[1]
    cmd = m.command[0][3:]  # removes 'set' prefix
    await Element_Network.set_metadata(m.from_user.id, cmd, value)
    await m.reply_text(f"✅ Set `{cmd}` to: {value}")
  

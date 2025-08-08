from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio
import os
from config import Config

@Client.on_message(filters.user(Config.BOT_OWNER) & filters.command("restart"))
async def restart_bot(_, m: Message):
    await m.reply_text("♻️ Restarting bot...")
    await asyncio.sleep(2)
    os.execl(sys.executable, sys.executable, *sys.argv)

@Client.on_message(filters.user(Config.BOT_OWNER) & filters.command("status"))
async def bot_status(_, m: Message):
    await m.reply_text("✅ Bot is up and running.")

@Client.on_message(filters.user(Config.BOT_OWNER) & filters.command("broadcast"))
async def broadcast(c, m: Message):
    if not m.reply_to_message:
        return await m.reply("Reply to a message to broadcast.")
    count = 0
    users = await Element_Network.get_all_users()
    for user_id in users:
        try:
            await m.reply_to_message.copy(chat_id=user_id)
            count += 1
        except:
            pass
    await m.reply_text(f"📣 Broadcast sent to {count} users.")
  

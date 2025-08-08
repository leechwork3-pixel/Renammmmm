from pyrogram import Client, filters
from pyrogram.types import Message
from helper.database import Element_Network
from config import Config

@Client.on_message(filters.private & filters.command("myplan"))
async def my_plan(c, m: Message):
    days = await Element_Network.check_premium(m.from_user.id)
    if days:
        await m.reply_text(f"🌟 You have Premium access for: {days} days.")
    else:
        await m.reply_text("🚫 You are not Premium.")

@Client.on_message(filters.user(Config.BOT_OWNER) & filters.command("addpremium"))
async def add_premium(c, m: Message):
    try:
        user = int(m.command[1])
        days = int(m.command[2])
    except:
        return await m.reply_text("Usage: /addpremium <user_id> <days>")
    await Element_Network.add_premium(user, days)
    await m.reply_text(f"✅ Premium added to `{user}` for {days} days.")

@Client.on_message(filters.user(Config.BOT_OWNER) & filters.command("rmpremium"))
async def remove_premium(c, m: Message):
    user = int(m.command[1])
    await Element_Network.remove_premium(user)
    await m.reply_text(f"❌ Premium removed for `{user}`.")

@Client.on_message(filters.user(Config.BOT_OWNER) & filters.command("premiumusers"))
async def view_premium_all(c, m: Message):
    users = await Element_Network.list_premium_users()
    if not users:
        return await m.reply("None found.")
    msg = "🌐 Premium Users:\n" + "\n".join([str(i) for i in users])
    await m.reply_text(msg)
  

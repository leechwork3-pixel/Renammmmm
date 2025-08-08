from pyrogram import Client, filters
from pyrogram.types import Message
from helper.database import Element_Network
from config import Config


@Client.on_message(filters.private & filters.command("myplan"))
async def my_plan(c: Client, m: Message):
    days = await Element_Network.check_premium(m.from_user.id)
    if days > 0:
        await m.reply_text(f"🌟 You have premium access for {days} day(s).")
    else:
        await m.reply_text("🚫 You are not a premium user yet.\nUse `/myplan` after upgrading.")


@Client.on_message(filters.user(Config.BOT_OWNER) & filters.command("addpremium"))
async def add_premium(c: Client, m: Message):
    if len(m.command) < 3:
        return await m.reply_text("❗ Usage: `/addpremium user_id days`\n\nExample: `/addpremium 123456789 30`")

    try:
        user_id = int(m.command[1])
        days = int(m.command[2])
        if days <= 0:
            return await m.reply_text("⚠️ Days must be a positive number.")
    except ValueError:
        return await m.reply_text("❗ Invalid input. Make sure to provide numeric user ID and days.")

    await Element_Network.add_premium(user_id, days)
    await m.reply_text(f"✅ Premium added to `{user_id}` for {days} day(s).")


@Client.on_message(filters.user(Config.BOT_OWNER) & filters.command("rmpremium"))
async def remove_premium(c: Client, m: Message):
    if len(m.command) < 2:
        return await m.reply_text("❗ Usage: `/rmpremium user_id`")

    try:
        user_id = int(m.command[1])
    except ValueError:
        return await m.reply_text("❗ Invalid user ID. Must be a number.")

    await Element_Network.remove_premium(user_id)
    await m.reply_text(f"❌ Premium removed for `{user_id}`.")


@Client.on_message(filters.user(Config.BOT_OWNER) & filters.command("premiumusers"))
async def list_premium_users(c: Client, m: Message):
    try:
        users = await Element_Network.list_premium_users()
        if not users:
            return await m.reply_text("📭 No premium users found.")
        text = "🌐 Premium Users:\n" + "\n".join([f"`{uid}`" for uid in users])
        await m.reply_text(text)
    except Exception as e:
        await m.reply_text("❌ Failed to load premium user list.")
        print(f"[PremiumUsersError] {e}")


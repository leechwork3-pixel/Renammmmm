import logging
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from helper.database import Element_Network
from config import Config

logger = logging.getLogger(__name__)

ADMIN_IDS = Config.ADMIN

@Client.on_message(filters.command("ban") & filters.user(ADMIN_IDS))
async def ban_user(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("Please reply to a user's message to ban them.")
    user_id = message.reply_to_message.from_user.id
    await Element_Network.ban_user(user_id)
    await message.reply_text(f"🚫 User `{user_id}` has been banned.")

@Client.on_message(filters.command("unban") & filters.user(ADMIN_IDS))
async def unban_user(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("Please reply to a user's message to unban them.")
    user_id = message.reply_to_message.from_user.id
    await Element_Network.unban_user(user_id)
    await message.reply_text(f"✅ User `{user_id}` has been unbanned.")

@Client.on_message(filters.command("search") & filters.user(ADMIN_IDS))
async def search_files(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("Please provide a search query, e.g. `/search filename`")
    query = " ".join(message.command[1:])
    storage_channel = Config.DUMP_CHANNEL
    count = 0
    async for msg in client.search_messages(storage_channel, query=query, filter="document"):
        count += 1
        await message.reply_document(msg.document.file_id, caption=msg.caption or "Document found")
        if count >= 5:
            await message.reply_text("Showing first 5 results.")
            break
    if count == 0:
        await message.reply_text("No files found matching your query.")

@Client.on_message(filters.command("leaderboard") & filters.user(ADMIN_IDS))
async def leaderboard(client: Client, message: Message):
    users = await Element_Network.get_all_users()
    if not users:
        return await message.reply_text("No users found.")
    leaderboard_data = []
    for user_id in users:
        queue = await Element_Network.get_queue(user_id)
        count = len(queue) if queue else 0
        leaderboard_data.append((user_id, count))
    leaderboard_data.sort(key=lambda x: x[1], reverse=True)
    text = "<b>User Upload Leaderboard:</b>\n\n"
    for i, (user_id, count) in enumerate(leaderboard_data[:10], 1):
        text += f"{i}. User ID: <code>{user_id}</code> - Files in queue: {count}\n"
    await message.reply_text(text, parse_mode="html")
  

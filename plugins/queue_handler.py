from pyrogram import Client, filters
from pyrogram.types import Message
from helper.database import Element_Network

@Client.on_message(filters.command("queue"))
async def show_queue(client: Client, message: Message):
    user_id = message.from_user.id
    queue = await Element_Network.get_queue(user_id)
    if not queue:
        return await message.reply_text("🗂 Your rename queue is empty.")
    text = "<b>Your Rename Queue:</b>\n\n"
    for idx, item in enumerate(queue, 1):
        file_name = item.get("file_name", "Unknown")
        text += f"{idx}. {file_name}\n"
    await message.reply_text(text, parse_mode="html")

@Client.on_message(filters.command("clearqueue"))
async def clear_user_queue(client: Client, message: Message):
    user_id = message.from_user.id
    await Element_Network.clear_queue(user_id)
    await message.reply_text("🗑️ Your rename queue has been cleared.")

@Client.on_message(filters.command("removefromqueue"))
async def remove_file_from_queue(client: Client, message: Message):
    user_id = message.from_user.id
    if len(message.command) < 2:
        return await message.reply_text("❗ Usage: /removefromqueue <file_name>")
    file_name = " ".join(message.command[1:])
    await Element_Network.remove_from_queue(user_id, file_name)
    await message.reply_text(f"🗑 Removed file '{file_name}' from your queue.")

@Client.on_message(filters.command("clearallqueue") & filters.user(Config.ADMIN))
async def clear_all_queues(client: Client, message: Message):
    await Element_Network.clear_all_user_queues()
    await message.reply_text("🗑️ Cleared all user rename queues.")
  

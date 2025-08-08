from pyrogram import Client, filters
from pyrogram.types import Message
from helper.database import Element_Network
from config import Config

# ─────────────────────────────────────────────
# /queue – Show the user's queued files
# ─────────────────────────────────────────────
@Client.on_message(filters.private & filters.command("queue"))
async def show_queue(client: Client, message: Message):
    """
    Show the current rename queue for a user.
    """
    user_id = message.from_user.id
    queue = await Element_Network.get_queue(user_id)
    if not queue:
        return await message.reply_text("🗂 Your rename queue is empty.")

    text = "<b>Your Rename Queue:</b>\n\n"
    for idx, item in enumerate(queue, 1):
        file_name = item.get("file_name", "Unknown")
        text += f"{idx}. {file_name}\n"

    await message.reply_text(text, parse_mode="html")

# ─────────────────────────────────────────────
# /clearqueue – Clear the user's own queue
# ─────────────────────────────────────────────
@Client.on_message(filters.private & filters.command("clearqueue"))
async def clear_user_queue(client: Client, message: Message):
    """
    Clear the current user's queue.
    """
    user_id = message.from_user.id
    await Element_Network.clear_queue(user_id)
    await message.reply_text("🗑️ Your rename queue has been cleared.")

# ─────────────────────────────────────────────
# /removefromqueue <filename> – Remove one item
# ─────────────────────────────────────────────
@Client.on_message(filters.private & filters.command("removefromqueue"))
async def remove_file_from_queue(client: Client, message: Message):
    """
    Remove a file by name from the user's queue.
    Usage: /removefromqueue filename.ext
    """
    user_id = message.from_user.id
    if len(message.command) < 2:
        return await message.reply_text("❗ Usage: /removefromqueue <file_name>")
    
    file_name = " ".join(message.command[1:]).strip()
    if not file_name:
        return await message.reply_text("❗ File name can't be empty.")
    
    removed = await Element_Network.remove_from_queue(user_id, file_name)
    if removed:
        await message.reply_text(f"🗑 Removed **{file_name}** from your queue.")
    else:
        await message.reply_text(f"⚠️ No entry found named **{file_name}** in your queue.")

# ─────────────────────────────────────────────
# /clearallqueue – Admin-only: Clears all user queues
# ─────────────────────────────────────────────
@Client.on_message(filters.command("clearallqueue") & filters.user(Config.ADMIN))
async def clear_all_queues(client: Client, message: Message):
    """
    Admin command to clear rename queues for all users.
    """
    await Element_Network.clear_all_user_queues()
    await message.reply_text("🛑 All user rename queues have been cleared (admin command).")
    

from pyrogram import Client, filters
from pyrogram.types import Message
from helper.database import Element_Network

# ─────────────────────────────────────────────
# Set custom caption
# ─────────────────────────────────────────────
@Client.on_message(filters.private & filters.command("set_caption"))
async def add_caption(client: Client, message: Message):
    if len(message.command) == 1:
        return await message.reply_text(
            "**Please provide a caption text after the command.**\n\n"
            "Example:\n`/set_caption 📕Name ➠ : {filename} \n\n🔗 Size ➠ : {filesize} \n\n⏰ Duration ➠ : {duration}`"
        )
    caption = message.text.split(' ', 1)[1].strip()
    await Element_Network.set_metadata(message.from_user.id, "caption", caption)
    await message.reply_text("✅ Caption saved successfully.")

# ─────────────────────────────────────────────
# Delete custom caption
# ─────────────────────────────────────────────
@Client.on_message(filters.private & filters.command("del_caption"))
async def delete_caption(client: Client, message: Message):
    caption = await Element_Network.get_caption(message.from_user.id)
    if not caption:
        return await message.reply_text("❌ You don't have any caption set.")
    await Element_Network.set_metadata(message.from_user.id, "caption", "")
    await message.reply_text("🗑️ Caption deleted successfully.")

# ─────────────────────────────────────────────
# View current caption
# ─────────────────────────────────────────────
@Client.on_message(filters.private & filters.command(['see_caption', 'view_caption', 'viewcaption']))
async def see_caption(client: Client, message: Message):
    caption = await Element_Network.get_caption(message.from_user.id)
    if caption:
        await message.reply_text(f"📋 Your current caption:\n\n`{caption}`")
    else:
        await message.reply_text("❌ You have no caption set.")

# ─────────────────────────────────────────────
# View current thumbnail
# ─────────────────────────────────────────────
@Client.on_message(filters.private & filters.command(['view_thumb', 'viewthumb']))
async def view_thumb(client: Client, message: Message):
    thumb = await Element_Network.get_thumbnail(message.from_user.id)
    if thumb:
        await client.send_photo(chat_id=message.chat.id, photo=thumb)
    else:
        await message.reply_text("❌ You don't have any thumbnail set.")

# ─────────────────────────────────────────────
# Delete custom thumbnail
# ─────────────────────────────────────────────
@Client.on_message(filters.private & filters.command(['del_thumb', 'delthumb']))
async def remove_thumb(client: Client, message: Message):
    await Element_Network.set_metadata(message.from_user.id, "thumbnail", "")
    await message.reply_text("🗑️ Thumbnail deleted successfully.")

# ─────────────────────────────────────────────
# Automatically save photo message as thumbnail
# ─────────────────────────────────────────────
@Client.on_message(filters.private & filters.photo)
async def add_thumb(client: Client, message: Message):
    mkn = await message.reply_text("⏳ Saving your thumbnail, please wait...")
    await Element_Network.set_metadata(message.from_user.id, "thumbnail", message.photo.file_id)
    await mkn.edit("✅ Thumbnail saved successfully.")
    

from pyrogram import Client, filters
from helper.database import Element_Network

@Client.on_message(filters.private & filters.command('set_caption'))
async def add_caption(client: Client, message):
    if len(message.command) == 1:
        return await message.reply_text(
            "**Please provide a caption text after the command.**\n\n"
            "Example:\n`/set_caption 📕Name ➠ : {filename} \n\n🔗 Size ➠ : {filesize} \n\n⏰ Duration ➠ : {duration}`"
        )
    caption = message.text.split(' ', 1)[1]
    await Element_Network.set_caption(message.from_user.id, caption=caption)
    await message.reply_text("✅ Caption saved successfully.")

@Client.on_message(filters.private & filters.command('del_caption'))
async def delete_caption(client: Client, message):
    caption = await Element_Network.get_caption(message.from_user.id)
    if not caption:
        return await message.reply_text("❌ You don't have any caption set.")
    await Element_Network.set_caption(message.from_user.id, caption=None)
    await message.reply_text("🗑️ Caption deleted successfully.")

@Client.on_message(filters.private & filters.command(['see_caption', 'view_caption']))
async def see_caption(client: Client, message):
    caption = await Element_Network.get_caption(message.from_user.id)
    if caption:
        await message.reply_text(f"📋 Your current caption:\n\n`{caption}`")
    else:
        await message.reply_text("❌ You have no caption set.")

@Client.on_message(filters.private & filters.command(['view_thumb', 'viewthumb']))
async def view_thumb(client: Client, message):
    thumb = await Element_Network.get_thumbnail(message.from_user.id)
    if thumb:
        await client.send_photo(chat_id=message.chat.id, photo=thumb)
    else:
        await message.reply_text("❌ You don't have any thumbnail set.")

@Client.on_message(filters.private & filters.command(['del_thumb', 'delthumb']))
async def remove_thumb(client: Client, message):
    await Element_Network.set_thumbnail(message.from_user.id, file_id=None)
    await message.reply_text("🗑️ Thumbnail deleted successfully.")

@Client.on_message(filters.private & filters.photo)
async def add_thumb(client: Client, message):
    mkn = await message.reply_text("⏳ Saving your thumbnail, please wait...")
    await Element_Network.set_thumbnail(message.from_user.id, file_id=message.photo.file_id)
    await mkn.edit("✅ Thumbnail saved successfully.")
  

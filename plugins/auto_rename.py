from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from helper.database import Element_Network

@Client.on_message(filters.private & filters.command("autorename"))
async def auto_rename_command(client: Client, message: Message):
    user_id = message.from_user.id

    is_premium = await Element_Network.check_premium(user_id)
    if is_premium == 0:
        return await message.reply_text(
            "❌ This is a premium-only feature.\n"
            "Contact @Shadow_Blank to upgrade your plan."
        )

    # Get the rename format from the command
    if len(message.command) < 2 or not message.text.split(" ", 1)[1].strip():
        return await message.reply_text(
            "**Usage:** `/autorename MyShow S01E01 {quality}{ext}`\n\n"
            "`{quality}`, `{ext}`, `{season}`, `{episode}` are replaceable tags.\n"
            "**Example:** `/autorename Naruto S{season}E{episode} [{quality}]`"
        )

    template = message.text.split(" ", 1)[1].strip()

    await Element_Network.set_format_template(user_id, template)
    await message.reply_text(
        f"✅ Rename template saved:\n`{template}`\n\nNow send me a file to rename!"
    )


@Client.on_message(filters.private & filters.command("setmedia"))
async def set_media_command(client: Client, message: Message):
    user_id = message.from_user.id

    is_premium = await Element_Network.check_premium(user_id)
    if is_premium == 0:
        return await message.reply_text(
            "❌ This is a premium-only feature.\n"
            "Contact @Shadow_Blank to upgrade your access."
        )

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📜 Document", callback_data="setmedia_document")],
        [InlineKeyboardButton("🎬 Video", callback_data="setmedia_video")],
        [InlineKeyboardButton("🎵 Audio", callback_data="setmedia_audio")]
    ])

    await message.reply_text(
        "🎯 Select your preferred media output:",
        reply_markup=keyboard
    )


@Client.on_callback_query(filters.regex(r"^setmedia_"))
async def handle_media_selection(client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    media_type = callback_query.data.split("_")[1]

    is_premium = await Element_Network.check_premium(user_id)
    if is_premium == 0:
        await callback_query.answer("Premium only! Upgrade via @Shadow_Blank", show_alert=True)
        return

    try:
        await Element_Network.set_metadata(user_id, "media_type", media_type)
        await callback_query.answer(f"Set to {media_type.title()}")
        await callback_query.message.edit_text(
            f"✅ Your media type preference is set to **{media_type.title()}**"
        )
    except Exception as e:
        await callback_query.answer("⚠️ Error", show_alert=True)
        await callback_query.message.edit_text("Something went wrong while saving your preference.")
        print(f"[setmedia] {user_id}: {e}")
        

from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)
from helper.database import Element_Network
from config import Config


# ─────────────────────────────────────────────
# /autorename — Set rename format (premium only)
# ─────────────────────────────────────────────
@Client.on_message(filters.private & filters.command("autorename"))
async def auto_rename_command(client: Client, message: Message):
    user_id = message.from_user.id

    # 🔐 Check premium access
    is_premium = await Element_Network.check_premium(user_id)
    if is_premium == 0:
        return await message.reply_text(
            "❌ This is a premium-only feature.\n"
            "Contact @Shadow_Blank to upgrade your plan."
        )

    # 📌 Check if format argument is provided
    try:
        template = message.text.split(" ", 1)[1].strip()
        if not template:
            raise ValueError
    except Exception:
        return await message.reply_text(
            "**Usage:** `/autorename {title}.S{season}E{episode} [{quality}]{ext}`\n\n"
            "`{season}` `{episode}` `{quality}` `{ext}` are placeholders.\n"
            "**Example:** `/autorename Naruto.S{season}E{episode}.{quality}{ext}`",
            parse_mode="markdown"
        )

    # ✅ Save template
    await Element_Network.set_format_template(user_id, template)
    await message.reply_text(
        f"✅ Auto Rename Template Saved:\n\n`{template}`\n\n"
        "Now send me a file to rename using this format!",
        parse_mode="markdown"
    )


# ─────────────────────────────────────────────
# /setmedia — Set default output type (premium)
# ─────────────────────────────────────────────
@Client.on_message(filters.private & filters.command("setmedia"))
async def set_media_command(client: Client, message: Message):
    user_id = message.from_user.id

    is_premium = await Element_Network.check_premium(user_id)
    if is_premium == 0:
        return await message.reply_text(
            "❌ This is a premium-only setting.\n"
            "Contact @Shadow_Blank to upgrade your access."
        )

    # 📋 Show media type options
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📄 Document", callback_data="setmedia_document"),
            InlineKeyboardButton("🎞 Video", callback_data="setmedia_video"),
            InlineKeyboardButton("🎵 Audio", callback_data="setmedia_audio")
        ]
    ])

    await message.reply_text(
        "🎯 Choose how you want renamed files to be sent:",
        reply_markup=keyboard
    )


# ─────────────────────────────────────────────
# Callback: Handle media selection
# ─────────────────────────────────────────────
@Client.on_callback_query(filters.regex(r"^setmedia_"))
async def handle_media_selection(client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    media_type = callback_query.data.split("_", 1)[1]  # document, video, audio

    is_premium = await Element_Network.check_premium(user_id)
    if is_premium == 0:
        await callback_query.answer(
            "⚠️ Premium required! Contact @Shadow_Blank to upgrade.",
            show_alert=True
        )
        return

    try:
        # 💾 Save media preference to DB
        await Element_Network.set_metadata(user_id, "media_type", media_type)
        await callback_query.answer(f"✅ Set to {media_type.title()}")
        await callback_query.message.edit_text(
            f"✅ Your output media type is now set to **{media_type.title()}**.",
            parse_mode="markdown"
        )
    except Exception as e:
        await callback_query.answer("⚠️ Failed to save preference.", show_alert=True)
        await callback_query.message.edit_text(
            "An error occurred while saving your setting. Please try again."
        )
        print(f"[SetMediaError] user_id={user_id} | error={e}")
        

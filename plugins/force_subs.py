from pyrogram import Client, filters
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from config import Config

IMAGE_URL = "https://i.ibb.co/gFQFknCN/d8a33273f73c.jpg"
CHANNELS = [ch.strip().lstrip("@") for ch in Config.FORCE_SUB_CHANNELS if ch.strip()]

@Client.on_message(filters.private & filters.create(lambda _, __, m: True))
async def force_sub_check(client: Client, message: Message):
    user_id = message.from_user.id
    not_joined = []

    for channel in CHANNELS:
        try:
            member = await client.get_chat_member(channel, user_id)
            if member.status in ("kicked", "left"):
                not_joined.append(channel)
        except UserNotParticipant:
            not_joined.append(channel)
        except Exception:
            continue

    if not_joined:
        buttons = [[InlineKeyboardButton(f"Join @{ch}", url=f"https://t.me/{ch}")] for ch in not_joined]
        buttons.append([InlineKeyboardButton("✔️ I've Joined", callback_data="check_subscription")])

        await message.reply_photo(
            photo=IMAGE_URL,
            caption=(
                "**🚫 You must join all required update channels to use this bot.**\n\n"
                "Please join the channels below and then click the ✔️ Joined button."
            ),
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    else:
        # User is subscribed to all required channels; proceed normally or do nothing
        pass

@Client.on_callback_query(filters.regex("^check_subscription$"))
async def check_subscription_status(client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    not_joined = []

    for channel in CHANNELS:
        try:
            member = await client.get_chat_member(channel, user_id)
            if member.status in ("kicked", "left"):
                not_joined.append(channel)
        except UserNotParticipant:
            not_joined.append(channel)
        except Exception:
            continue

    if not not_joined:
        await callback_query.message.edit_caption(
            caption="✅ You have joined all required channels.\nYou can now use /start to continue!"
        )
    else:
        await callback_query.answer(
            "⚠️ You have not joined all required channels yet. Please join and try again.",
            show_alert=True
        )
        

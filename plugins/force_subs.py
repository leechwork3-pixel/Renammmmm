from pyrogram import Client, filters
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from config import Config

IMAGE_URL = "https://i.ibb.co/gFQFknCN/d8a33273f73c.jpg"
CHANNELS = [x.strip().lstrip("@") for x in Config.FORCE_SUB_CHANNELS]


@Client.on_message(filters.private & filters.create(lambda _, __, m: True))
async def force_sub_check(client: Client, message: Message):
    user_id = message.from_user.id
    not_joined = []

    for ch in CHANNELS:
        try:
            member = await client.get_chat_member(ch, user_id)
            if member.status in ("kicked", "left"):
                not_joined.append(ch)
        except UserNotParticipant:
            not_joined.append(ch)

    if not_joined:
        buttons = [
            [InlineKeyboardButton(f"Join @{ch}", url=f"https://t.me/{ch}")]
            for ch in not_joined
        ]
        buttons.append([InlineKeyboardButton("✔️ Joined", callback_data="check_subscription")])

        return await message.reply_photo(
            photo=IMAGE_URL,
            caption=(
                "**🚫 You're not joined to all required update channels.**\n\n"
                "Please join them and then click **✔️ Joined** button below."
            ),
            reply_markup=InlineKeyboardMarkup(buttons)
        )


@Client.on_callback_query(filters.regex("check_subscription"))
async def check_subscription_status(client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    not_joined = []

    for ch in CHANNELS:
        try:
            member = await client.get_chat_member(ch, user_id)
            if member.status in ("kicked", "left"):
                not_joined.append(ch)
        except UserNotParticipant:
            not_joined.append(ch)

    if not not_joined:
        await callback_query.message.edit_caption(
            caption="✅ You’ve joined all required channels. Now use /start to continue!"
        )
    else:
        await callback_query.answer("⚠️ Still missing one or more joins.", show_alert=True)
        

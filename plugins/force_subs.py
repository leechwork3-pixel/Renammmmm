from pyrogram import Client, filters
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from config import Config

# ✅ Thumbnail or banner to show in the join prompt
IMAGE_URL = "https://i.ibb.co/gFQFknCN/d8a33273f73c.jpg"

# ✅ Clean and normalize force-subscribe channel list
CHANNELS = []
for ch in Config.FORCE_SUB_CHANNELS:
    ch_str = str(ch).strip().lstrip("@")
    if ch_str:
        CHANNELS.append(ch_str)

# ✅ Check user subscription when they send private messages
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
        except Exception:
            continue

    if not_joined:
        # 🔘 Join buttons for each missing channel
        buttons = [[InlineKeyboardButton(f"Join @{ch}", url=f"https://t.me/{ch}")] for ch in not_joined]
        # ➕ Add a 'Joined' button to re-check
        buttons.append([InlineKeyboardButton("✔️ I've Joined", callback_data="check_subscription")])

        await message.reply_photo(
            photo=IMAGE_URL,
            caption=(
                "**🚫 You must join all required update channels to use this bot.**\n\n"
                "Please join the channels below, then click **✔️ I've Joined** to continue."
            ),
            reply_markup=InlineKeyboardMarkup(buttons)
        )


# ✅ Callback: Re-check user joins after clicking "I've Joined"
@Client.on_callback_query(filters.regex("^check_subscription$"))
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
        except Exception:
            continue

    if not not_joined:
        await callback_query.message.edit_caption(
            caption="✅ You have joined all required channels!\nYou can now use /start to continue."
        )
    else:
        await callback_query.answer(
            text="⚠️ You still haven't joined all required channels. Please join first.",
            show_alert=True
        )


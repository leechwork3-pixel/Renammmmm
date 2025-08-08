from pyrogram import Client, filters
from pyrogram.errors import UserNotParticipant
from config import Config

CHANNELS = [i for i in Config.FORCE_SUB_CHANNELS if i]

@Client.on_message(filters.private & ~filters.command("start"))
async def enforce_subs(client, message):
    for ch in CHANNELS:
        try:
            await client.get_chat_member(ch, message.from_user.id)
        except UserNotParticipant:
            return await message.reply_text(
                f"🔒 You must join @{ch} to use this bot.",
                disable_web_page_preview=True
            )
          

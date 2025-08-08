import os
import sys
import time
import asyncio
import logging
import datetime

from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid

from config import Config, Txt
from helper.database import Element_Network

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ADMIN_USER_ID = Config.ADMIN
is_restarting = False  # Lock flag for restart control


# ─────────────────────────────────────────────
# /restart — Bot Owner: Restart the bot 
# ─────────────────────────────────────────────
@Client.on_message(filters.private & filters.command("restart") & filters.user(ADMIN_USER_ID))
async def restart_bot(b: Client, m: Message):
    global is_restarting
    if not is_restarting:
        is_restarting = True
        await m.reply_text("♻️ Restarting AutoRenameBot...")
        await asyncio.sleep(1)
        b.stop()
        time.sleep(2)
        os.execl(sys.executable, sys.executable, *sys.argv)


# ─────────────────────────────────────────────
# /tutorial — Show Format Template Guide
# ─────────────────────────────────────────────
@Client.on_message(filters.private & filters.command("tutorial"))
async def tutorial(bot: Client, message: Message):
    user_id = message.from_user.id
    format_template = await Element_Network.get_format_template(user_id)
    format_template = format_template or "{filename}"  # default fallback

    # If Txt.FILE_NAME_TXT uses .format(), inject safely
    try:
        text = Txt.FILE_NAME_TXT.format(format_template=format_template)
    except KeyError:
        text = Txt.FILE_NAME_TXT

    await message.reply_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("• ᴏᴡɴᴇʀ", url="https://t.me/Shadow_Blank"),
                InlineKeyboardButton("• ᴛᴜᴛᴏʀɪᴀʟ", url="https://t.me/Element_Network")
            ]
        ])
    )


# ─────────────────────────────────────────────
# /stats or /status — Bot Owner: Show Bot Health
# ─────────────────────────────────────────────
@Client.on_message(filters.command(["stats", "status"]) & filters.user(ADMIN_USER_ID))
async def get_stats(bot: Client, message: Message):
    total_users = await Element_Network.total_users_count()
    uptime = time.strftime("%Hh %Mm %Ss", time.gmtime(time.time() - bot.uptime))
    start = time.time()
    status_msg = await message.reply("🧮 Calculating status...")
    end = time.time()

    ping_time = (end - start) * 1000
    await status_msg.edit(
        f"**📊 Bot Status Report**\n\n"
        f"⏱ Uptime: `{uptime}`\n"
        f"📡 Ping: `{ping_time:.2f} ms`\n"
        f"👥 Users: `{total_users}`"
    )


# ─────────────────────────────────────────────
# /broadcast (reply) — Owner: Send message to all 
# ─────────────────────────────────────────────
@Client.on_message(filters.command("broadcast") & filters.user(ADMIN_USER_ID) & filters.reply)
async def broadcast_handler(bot: Client, m: Message):
    await bot.send_message(
        Config.LOG_CHANNEL,
        f"📢 Broadcast started by {m.from_user.mention} (`{m.from_user.id}`)"
    )

    broadcast_msg = m.reply_to_message
    all_users = await Element_Network.get_all_users()
    total_users = len(all_users)

    status = await m.reply_text("📤 Broadcast in progress...")
    success = failed = done = 0
    start_time = time.time()

    async for user in all_users:
        user_id = user['_id']
        status_code = await send_msg(user_id, broadcast_msg)

        if status_code == 200:
            success += 1
        else:
            failed += 1
            if status_code == 400:
                await Element_Network.delete_user(user_id)

        done += 1
        if done % 20 == 0 or done == total_users:
            await status.edit(
                f"📡 Broadcasting\n\n"
                f"✅ Success: `{success}`\n"
                f"❌ Failed: `{failed}`\n"
                f"📈 Progress: `{done}/{total_users}`"
            )

    duration = str(datetime.timedelta(seconds=int(time.time() - start_time)))
    await status.edit(
        f"✅ **Broadcast Complete**\n\n"
        f"🕒 Duration: `{duration}`\n"
        f"👥 Total: `{total_users}`\n"
        f"✅ Sent: `{success}`\n"
        f"❌ Failed: `{failed}`"
    )


# ─────────────────────────────────────────────
# Send a message to a user safely
# ─────────────────────────────────────────────
async def send_msg(user_id, message):
    try:
        await message.copy(chat_id=int(user_id))
        return 200
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await send_msg(user_id, message)
    except (InputUserDeactivated, UserIsBlocked, PeerIdInvalid):
        logger.info(f"[Skip] {user_id} is inactive or blocked.")
        return 400
    except Exception as e:
        logger.error(f"[Error] {user_id} → {e}")
        return 500
        

import os
import sys
import time
import asyncio
import logging
import datetime

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid

from config import Config, Txt
from helper.database import Element_Network

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ADMIN_USER_ID = Config.BOT_OWNER
is_restarting = False


# ─────────────────────────────────────────────
# /restart — Admin: Restart the bot forcefully
# ─────────────────────────────────────────────
@Client.on_message(filters.private & filters.command("restart") & filters.user(ADMIN_USER_ID))
async def restart_bot(b: Client, m: Message):
    global is_restarting
    if not is_restarting:
        is_restarting = True
        await m.reply_text("♻️ Restarting AutoRenameBot...")
        await asyncio.sleep(1)
        b.stop()  # Optional: cleanup
        time.sleep(2)
        os.execl(sys.executable, sys.executable, *sys.argv)


# ─────────────────────────────────────────────
# /tutorial — Show format template with guide
# ─────────────────────────────────────────────
@Client.on_message(filters.private & filters.command("tutorial"))
async def tutorial_handler(bot: Client, message: Message):
    user_id = message.from_user.id
    template = await Element_Network.get_format_template(user_id)

    await message.reply_text(
        text=Txt.FILE_NAME_TXT.format(
            format_template=template if template else "{filename}"
        ),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("• Owner", url="https://t.me/Shadow_Blank"),
             InlineKeyboardButton("• Tutorial", url="https://t.me/Shadow_Blank")]
        ])
    )


# ─────────────────────────────────────────────
# /stats or /status — Admin: Bot health summary
# ─────────────────────────────────────────────
@Client.on_message(filters.command(["stats", "status"]) & filters.user(ADMIN_USER_ID))
async def get_stats(bot: Client, message: Message):
    start = time.time()
    uptime = time.strftime("%Hh %Mm %Ss", time.gmtime(time.time() - bot.start_time))

    users = await Element_Network.get_all_users()
    total_users = len(users)

    ping_msg = await message.reply("📡 Gathering bot stats...")
    end = time.time()
    ping_ms = (end - start) * 1000

    await ping_msg.edit(
        f"**📊 Bot Status Report**\n\n"
        f"🕒 Uptime: `{uptime}`\n"
        f"📶 Ping: `{ping_ms:.2f} ms`\n"
        f"👥 Total Users: `{total_users}`"
    )


# ─────────────────────────────────────────────
# /broadcast — Admin-only user broadcast
# REQUIRES: Reply to message to send
# ─────────────────────────────────────────────
@Client.on_message(filters.command("broadcast") & filters.user(ADMIN_USER_ID) & filters.reply)
async def broadcast_handler(bot: Client, m: Message):
    start_time = time.time()

    all_users = await Element_Network.get_all_users()
    broadcast_msg = m.reply_to_message
    total = len(all_users)

    log_text = f"📢 Broadcast initiated by {m.from_user.mention} (`{m.from_user.id}`)"
    await bot.send_message(Config.LOG_CHANNEL, log_text)

    report = await m.reply_text("📣 Broadcast starting...")
    success = failed = 0

    for i, user_id in enumerate(all_users, start=1):
        result = await send_msg(user_id, broadcast_msg)
        if result == 200:
            success += 1
        elif result == 400:
            failed += 1
            await Element_Network.remove_premium(user_id)  # Cleanup
        elif result == 500:
            failed += 1

        # Update report every 20 users
        if i % 20 == 0 or i == total:
            await report.edit(
                f"📤 Broadcasting...\n"
                f"✅ Sent: `{success}`\n"
                f"❌ Failed: `{failed}`\n"
                f"Progress: {i}/{total}"
            )

    duration = str(datetime.timedelta(seconds=int(time.time() - start_time)))
    await report.edit(
        f"📬 **Broadcast Completed**\n\n"
        f"⏱ Duration: `{duration}`\n"
        f"👥 Total: `{total}`\n✅ Sent: `{success}`\n❌ Failed: `{failed}`"
    )


# ─────────────────────────────────────────────
# Send copied message to user with proper checks
# ─────────────────────────────────────────────
async def send_msg(user_id, message):
    try:
        await message.copy(chat_id=int(user_id))
        return 200
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await send_msg(user_id, message)
    except (InputUserDeactivated, UserIsBlocked, PeerIdInvalid):
        return 400
    except Exception as e:
        logger.error(f"[Broadcast Error] User: {user_id} | Error: {e}")
        return 500
        

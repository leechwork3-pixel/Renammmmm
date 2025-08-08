from config import Config, Txt
from helper.database import Element_Network
from pyrogram.types import Message
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid
import os, sys, time, asyncio, logging, datetime
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ADMIN_USER_ID = Config.BOT_OWNER

is_restarting = False

@Client.on_message(filters.private & filters.command("restart") & filters.user(ADMIN_USER_ID))
async def restart_bot(b, m: Message):
    global is_restarting
    if not is_restarting:
        is_restarting = True
        await m.reply_text("♻️ Restarting AutoRenameBot...")
        await asyncio.sleep(1)
        b.stop()
        time.sleep(2)
        os.execl(sys.executable, sys.executable, *sys.argv)

@Client.on_message(filters.private & filters.command("tutorial"))
async def tutorial_handler(bot: Client, message: Message):
    user_id = message.from_user.id
    template = await Element_Network.get_format_template(user_id)
    await message.reply_text(
        text=Txt.FILE_NAME_TXT.format(format_template=template if template else "{filename}"),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("• Owner", url="https://t.me/Shadow_Blank"),
                InlineKeyboardButton("• Tutorial", url="https://t.me/Shadow_Blank")
            ]
        ])
    )

@Client.on_message(filters.command(["stats", "status"]) & filters.user(ADMIN_USER_ID))
async def get_stats(bot: Client, message: Message):
    start = time.time()
    uptime = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - bot.start_time))
    users = await Element_Network.get_all_users()
    total_users = len(users)
    ping_msg = await message.reply("Getting stats...")
    end = time.time()
    ping_ms = (end - start) * 1000

    await ping_msg.edit(
        f"**📊 Bot Status:**\n"
        f"• Uptime: `{uptime}`\n"
        f"• Ping: `{ping_ms:.2f} ms`\n"
        f"• Total Users: `{total_users}`"
    )

@Client.on_message(filters.command("broadcast") & filters.user(ADMIN_USER_ID) & filters.reply)
async def broadcast_handler(bot: Client, m: Message):
    await bot.send_message(Config.LOG_CHANNEL, f"📢 Broadcast started by {m.from_user.mention} (`{m.from_user.id}`)")
    all_users = await Element_Network.get_all_users()
    broadcast_msg = m.reply_to_message

    done = success = failed = 0
    report_msg = await m.reply_text("📤 Broadcast started...")
    start_time = time.time()
    total = len(all_users)

    for user_id in all_users:
        result = await send_msg(user_id, broadcast_msg)
        if result == 200:
            success += 1
        elif result == 400:
            failed += 1
            await Element_Network.remove_premium(user_id)  # Assuming clean-up of dead users
        done += 1
        if done % 20 == 0:
            await report_msg.edit(
                f"Broadcast Progress:\n"
                f"Sent: `{done}/{total}`\n✅ Success: `{success}`\n❌ Failed: `{failed}`"
            )

    duration = datetime.timedelta(seconds=int(time.time() - start_time))
    await report_msg.edit(f"📬 **Broadcast Complete**\n"
                          f"Duration: `{duration}`\n"
                          f"Total: `{total}` | ✅ `{success}` | ❌ `{failed}`")

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
        logger.error(f"Broadcast error for {user_id}: {e}")
        return 500
        

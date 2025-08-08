import asyncio
import logging
import os
import sys
import threading
import time
from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler, HTTPServer
from importlib import import_module

from pyrogram import Client
from pyrogram.enums import ParseMode
from pyrogram.errors import PeerIdInvalid, ChannelPrivate, ChatAdminRequired
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from pytz import timezone

from config import Config
from plugins import ALL_MODULES
from logging.config import fileConfig

# ─────────────── Logging Setup ───────────────
fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)

# ─────────────── Health Check Server ───────────────
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_health_server():
    port = getattr(Config, "PORT", 8080)
    try:
        server = HTTPServer(("0.0.0.0", port), HealthHandler)
        logger.info(f"🩺 Health check server running on port {port}.")
        server.serve_forever()
    except Exception as e:
        logger.error(f"❌ Health check server error: {e}")

threading.Thread(target=run_health_server, daemon=True).start()

# ─────────────── Safe Send Message ───────────────
async def safe_send_startup_message(bot, chat_id, message: str):
    try:
        await bot.send_message(chat_id, message)
        logger.info(f"[Startup ✅] Message sent to {chat_id}")
    except PeerIdInvalid:
        logger.warning(f"[Startup ⚠️] Peer ID invalid → {chat_id}")
    except ChannelPrivate:
        logger.warning(f"[Startup ⚠️] Channel private or inaccessible → {chat_id}")
    except ChatAdminRequired:
        logger.warning(f"[Startup ⚠️] Bot not admin in → {chat_id}")
    except Exception as e:
        logger.warning(f"[Startup ⚠️] Failed to send to {chat_id}: {e}")

# ─────────────── Bot Client ───────────────
class Bot(Client):
    def __init__(self):
        super().__init__(
            name="AutoRenameBot",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            workers=200,
            plugins=dict(root="plugins"),
            sleep_threshold=15,
            parse_mode=ParseMode.HTML,
        )
        self.start_time = time.time()

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.mention = me.mention
        self.username = me.username

        uptime_seconds = int(time.time() - self.start_time)
        uptime_str = str(timedelta(seconds=uptime_seconds))

        now = datetime.now(timezone("Asia/Kolkata"))
        date_str = now.strftime("%d %B, %Y")
        time_str = now.strftime("%I:%M:%S %p")

        caption = (
            "**ᴀɴʏᴀ ɪs ʀᴇsᴛᴀʀᴛᴇᴅ ᴀɢᴀɪɴ!**\n\n"
            f"ɪ ᴅɪᴅɴ'ᴛ sʟᴇᴘᴛ sɪɴᴄᴇ: `{uptime_str}`\n"
            f"🕓 {date_str} — {time_str} IST"
        )

        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇs", url="https://t.me/Element_Network")]
        ])

        notify_chats = [Config.LOG_CHANNEL, Config.SUPPORT_CHAT]

        for chat_id in notify_chats:
            try:
                await self.send_photo(
                    chat_id=chat_id,
                    photo=Config.START_PIC or "",
                    caption=caption,
                    reply_markup=buttons,
                )
                logger.info(f"[Startup ✅] Sent startup photo to {chat_id}")
            except Exception as e:
                logger.warning(f"[Startup ⚠️] Failed to send startup photo to {chat_id}: {e}")

        for module in ALL_MODULES:
            import_module(f"plugins.{module}")
            logger.info(f"✅ Loaded plugin: {module}")

        logger.info(f"🤖 AutoRenameBot @{self.username} started successfully.")

    async def stop(self, *args):
        await super().stop()
        logger.warning("🛑 AutoRenameBot has stopped.")

    def run(self):
        super().run()

# ─────────────── Main ───────────────
if __name__ == "__main__":
    try:
        Bot().run()
    except KeyboardInterrupt:
        logger.info("Interrupted. Shutting down...")
        sys.exit()
        

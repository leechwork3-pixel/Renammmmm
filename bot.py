import asyncio
import logging
import sys
import time
import threading
from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler, HTTPServer

from pyrogram import Client
from pyrogram.enums import ParseMode
from pyrogram.errors import PeerIdInvalid, ChannelPrivate, ChatAdminRequired
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import Config
from plugins import ALL_MODULES
from importlib import import_module
from logging.config import fileConfig
from pytz import timezone

# ─────────────────────────────────────────────────────
# Logging Setup
# ─────────────────────────────────────────────────────
fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────
# Startup Health Check Server (for platform health probes)
# ─────────────────────────────────────────────────────
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")


def run_health_server():
    try:
        server = HTTPServer(('0.0.0.0', Config.PORT if hasattr(Config, "PORT") else 8080), HealthHandler)
        logger.info(f"🩺 Health check server running on port {Config.PORT if hasattr(Config, 'PORT') else 8080}.")
        server.serve_forever()
    except Exception as e:
        logger.error(f"❌ Error starting health check server: {e}")


threading.Thread(target=run_health_server, daemon=True).start()


# ─────────────────────────────────────────────────────
# Safe message sender utility for startup notifications
# ─────────────────────────────────────────────────────
async def safe_send_startup_message(bot, chat_id, message: str):
    try:
        await bot.send_message(chat_id, message)
        logger.info(f"[Startup ✅] Message sent to {chat_id}")
    except PeerIdInvalid:
        logger.warning(f"[Startup ⚠️] Invalid Peer ID → {chat_id}")
    except ChannelPrivate:
        logger.warning(f"[Startup ⚠️] Channel private or inaccessible → {chat_id}")
    except ChatAdminRequired:
        logger.warning(f"[Startup ⚠️] Bot not admin in → {chat_id}")
    except Exception as e:
        logger.error(f"[Startup ⚠️] Error sending to {chat_id}: {e}")


SUPPORT_CHAT_ID = os.getenv("SUPPORT_CHAT")
try:
    SUPPORT_CHAT_ID = int(SUPPORT_CHAT_ID)
except Exception:
    SUPPORT_CHAT_ID = SUPPORT_CHAT_ID  # Keep as string if not integer


# ─────────────────────────────────────────────────────
# Main Bot Client class
# ─────────────────────────────────────────────────────
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

        # Calculate uptime string
        uptime_seconds = int(time.time() - self.start_time)
        uptime_string = str(timedelta(seconds=uptime_seconds))

        # Prepare startup notification caption and buttons
        curr = datetime.now(timezone("Asia/Kolkata"))
        date_str = curr.strftime('%d %B, %Y')
        time_str = curr.strftime('%I:%M:%S %p')

        caption = (
            "**ᴀɴʏᴀ ɪs ʀᴇsᴛᴀʀᴛᴇᴅ ᴀɢᴀɪɴ  !**\n\n"
            f"ɪ ᴅɪᴅɴ'ᴛ sʟᴇᴘᴛ sɪɴᴄᴇ: `{uptime_string}`\n\n"
            f"Date: {date_str}\nTime: {time_str} IST"
        )

        buttons = InlineKeyboardMarkup(
            [[InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇs", url="https://t.me/techak_support")]]
        )

        # Send startup photo message to log and support chats
        for chat_id in [Config.LOG_CHANNEL, SUPPORT_CHAT_ID]:
            try:
                await self.send_photo(
                    chat_id=chat_id,
                    photo=Config.START_PIC or "",
                    caption=caption,
                    reply_markup=buttons
                )
                logger.info(f"[Startup ✅] Sent startup photo to {chat_id}")
            except Exception as e:
                logger.warning(f"[Startup ⚠️] Failed to send startup photo to {chat_id}: {e}")

        # Load all plugins dynamically
        for module_name in ALL_MODULES:
            import_module(f"plugins.{module_name}")
            logger.info(f"✅ Loaded plugin: {module_name}")

        logger.info(f"🤖 AutoRenameBot @{self.username} started successfully.")

    async def stop(self, *args):
        await super().stop()
        logger.info("🛑 AutoRenameBot has stopped.")

    def run(self):
        super().run()


# ─────────────────────────────────────────────────────
# Launch the bot
# ─────────────────────────────────────────────────────
if __name__ == "__main__":
    try:
        Bot().run()
    except KeyboardInterrupt:
        logger.info("Interrupted manually. Exiting...")
        sys.exit()
        

import asyncio
import logging
import sys
import time

from pyrogram import Client
from pyrogram.enums import ParseMode
from config import Config
from plugins import ALL_MODULES  # dynamically loads all plugin files
from importlib import import_module
from logging.config import fileConfig

# Optional: Configure logging from logging.conf
fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────
# STARTUP MESSAGE CHECKER
# ─────────────────────────────────────────────────────
from pyrogram.errors import PeerIdInvalid, ChannelPrivate, ChatAdminRequired


async def safe_send_startup_message(bot, chat_id, message: str):
    try:
        await bot.send_message(chat_id, message)
        print(f"[Startup ✅] Sent to {chat_id}")
    except PeerIdInvalid:
        print(f"[Startup ⚠️] Peer ID invalid → {chat_id}")
    except ChannelPrivate:
        print(f"[Startup ⚠️] Channel is private or inaccessible → {chat_id}")
    except ChatAdminRequired:
        print(f"[Startup ⚠️] Bot not admin in → {chat_id}")
    except Exception as e:
        print(f"[Startup ⚠️] Error sending to {chat_id} → {e}")


# ─────────────────────────────────────────────────────
# MAIN BOT CLIENT
# ─────────────────────────────────────────────────────
class Bot(Client):
    def __init__(self):
        super().__init__(
            name="AutoRenameBot",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            in_memory=True,
            parse_mode=ParseMode.HTML,
            plugins=dict(root="plugins")
        )
        self.start_time = time.time()

    async def start(self):
        await super().start()
        logger.info("🤖 AutoRenameBot has started!")

        # Safe check: validate log and dump channels
        await safe_send_startup_message(self, Config.LOG_CHANNEL, "✅ Bot successfully started!")
        if Config.DUMP_CHANNEL:
            await safe_send_startup_message(self, Config.DUMP_CHANNEL, "📥 Dump channel connected.")

        # Load helper modules or init queues if needed
        for module in ALL_MODULES:
            import_module(f"plugins.{module}")
            logger.info(f"✅ Loaded plugin: {module}")

    async def stop(self, *args):
        await super().stop()
        logger.warning("🛑 AutoRenameBot has stopped.")

    def run(self):
        super().run()


# ─────────────────────────────────────────────────────
# LAUNCH BOT
# ─────────────────────────────────────────────────────
if __name__ == "__main__":
    try:
        Bot().run()
    except KeyboardInterrupt:
        logger.info("Interrupted manually. Exiting...")
        sys.exit()
        

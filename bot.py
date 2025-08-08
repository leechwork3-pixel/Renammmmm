import os
import time
from datetime import datetime, timedelta
from pytz import timezone
from aiohttp import web
from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config

try:
    from route import web_server
except ImportError:
    web_server = None  # Disable webhook if route.py missing

SUPPORT_CHAT = Config.SUPPORT_CHAT
PORT = Config.PORT

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="AutoRenameBot",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            workers=64,
            plugins={"root": "plugins"},
            sleep_threshold=15
        )
        self.start_time = time.time()

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.mention = me.mention
        self.username = me.username

        # Start webhook server if needed
        if Config.WEBHOOK and web_server:
            runner = web.AppRunner(await web_server())
            await runner.setup()
            await web.TCPSite(runner, "0.0.0.0", PORT).start()

        uptime_seconds = int(time.time() - self.start_time)
        uptime_string = str(timedelta(seconds=uptime_seconds))

        for chat_id in filter(None, [Config.LOG_CHANNEL, SUPPORT_CHAT]):
            try:
                now = datetime.now(timezone("Asia/Kolkata"))
                await self.send_photo(
                    chat_id=chat_id,
                    photo=Config.START_PIC,
                    caption=(
                        f"**🤖 AutoRenameBot Restarted Successfully!**\n\n"
                        f"👤: {me.mention}\n"
                        f"⏰ Uptime: `{uptime_string}`\n"
                        f"📆 Date: `{now.strftime('%d %B %Y, %I:%M:%S %p')}`"
                    ),
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("🚀 Updates", url="https://t.me/Shadow_Blank")]
                    ])
                )
            except Exception as e:
                print(f"[Startup] Couldn't send log message: {e}")

if __name__ == "__main__":
    Bot().run()
    

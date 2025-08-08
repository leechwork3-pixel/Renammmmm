import os
import time
from datetime import datetime, timedelta
from pytz import timezone
from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiohttp import web
from config import Config
from route import web_server

SUPPORT_CHAT = Config.SUPPORT_CHAT
PORT = Config.PORT


class Bot(Client):
    def __init__(self):
        super().__init__(
            name="AutoRenameBot",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            workers=64,  # Adjust as needed based on host environment
            plugins={"root": "plugins"},
            sleep_threshold=15,
        )
        self.start_time = time.time()
        self.uptime = time.time()

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.mention = me.mention
        self.username = me.username

        if Config.WEBHOOK:
            runner = web.AppRunner(await web_server())
            await runner.setup()
            await web.TCPSite(runner, "0.0.0.0", PORT).start()

        uptime_seconds = int(time.time() - self.start_time)
        uptime_string = str(timedelta(seconds=uptime_seconds))

        for chat_id in [Config.LOG_CHANNEL, SUPPORT_CHAT]:
            try:
                now = datetime.now(timezone("Asia/Kolkata"))
                await self.send_photo(
                    chat_id=chat_id,
                    photo=Config.START_PIC,
                    caption=(
                        f"**🤖 AutoRenameBot Restarted Successfully!**\n\n"
                        f"👤: {me.mention}\n"
                        f"⏰: `{uptime_string}`\n"
                        f"📆: `{now.strftime('%d %B %Y, %I:%M:%S %p')}`"
                    ),
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("🚀 Updates", url="https://t.me/Shadow_Blank")]
                    ])
                )
            except Exception as e:
                print(f"[Startup] Couldn't send log message: {e}")


Bot().run()

from aiohttp import web
from pyrogram import Client
from config import Config

# Import the running instance from main bot script if needed
BOT = Client("AutoRenameBot")

# 🔁 Health check ping route (GET request)
async def handle_root(request):
    return web.Response(text="✅ AutoRenameBot is alive and responding.")

# 📥 Telegram webhook endpoint (POST request)
async def webhook_handler(request):
    try:
        data = await request.json()
        await BOT.process_update(data)
        return web.Response(status=200)
    except Exception as e:
        print("[Webhook Error]", e)
        return web.Response(status=500, text="❌ Failed processing update.")

# 🌐 Initialize aiohttp web application
async def web_server():
    app = web.Application()
    app.router.add_get("/", handle_root)
    app.router.add_post(f"/{Config.BOT_TOKEN}", webhook_handler)
    return app
    

from aiohttp import web
from pyrogram import Client

BOT = Client("AutoRenameBot")

async def ping(request):
    return web.Response(text="🤖 Bot is alive.")

async def webhook_handler(request):
    await BOT.process_update(await request.json())
    return web.Response()

async def web_server():
    app = web.Application()
    app.router.add_get("/", ping)
    app.router.add_post("/bot", webhook_handler)
    return app
  

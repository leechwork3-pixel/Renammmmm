from pyrogram import Client, filters
from pyrogram.types import Message
from helper.database import Element_Network

@Client.on_message(filters.private & filters.command("startsequence"))
async def start_seq(c, m: Message):
    await Element_Network.start_sequence(m.from_user.id)
    await m.reply_text("📥 Sequence mode started.\nSend each episode in order.")

@Client.on_message(filters.private & filters.command("endsequence"))
async def end_seq(c, m: Message):
    files = await Element_Network.end_sequence(m.from_user.id)
    if files:
        for f in files:
            await c.send_document(m.chat.id, document=f["file_id"], caption=f.get("caption", ""))
    else:
        await m.reply("❌ Sequence was empty.")

@Client.on_message(filters.private & filters.command("cancelsequence"))
async def cancel_seq(c, m: Message):
    await Element_Network.cancel_sequence(m.from_user.id)
    await m.reply_text("❌ Sequence cancelled.")

@Client.on_message(filters.private & filters.command("showsequence"))
async def show_seq(c, m: Message):
    files = await Element_Network.get_sequence(m.from_user.id)
    if not files:
        return await m.reply_text("🔹 No files in sequence yet.")
    out = "\n".join([f"{i+1}. {f['file_name']}" for i, f in enumerate(files)])
    await m.reply_text(f"📋 Files so far:\n\n{out}")
  

from pyrogram import Client, filters
from pyrogram.types import Message
from helper.database import Element_Network
from config import Config

# ─────────────────────────────────────────────
# /startsequence – Start multi-file rename mode
# ─────────────────────────────────────────────
@Client.on_message(filters.private & filters.command("startsequence"))
async def start_sequence(c: Client, m: Message):
    """
    Starts a new renaming sequence for the user.
    """
    try:
        await Element_Network.start_sequence(m.from_user.id)
        await m.reply_text(
            "🔄 <b>Sequence mode started!</b>\n\n"
            "Now send your files one by one.\n"
            "When you're done, send /endsequence to process them.",
            parse_mode="html"
        )
    except Exception as e:
        await m.reply_text("❌ Failed to start sequence mode.")
        print(f"[startsequence error] {e}")

# ─────────────────────────────────────────────
# /endsequence – Finish and upload files in order
# ─────────────────────────────────────────────
@Client.on_message(filters.private & filters.command("endsequence"))
async def end_sequence(c: Client, m: Message):
    """
    Ends the sequence and sends files back to the user (in order).
    """
    try:
        files = await Element_Network.end_sequence(m.from_user.id)

        if not files:
            return await m.reply_text("ℹ️ Sequence is empty. Nothing to send.")

        await m.reply_text(f"📦 Ending sequence and sending {len(files)} file(s)...")

        for file in files:
            try:
                await c.send_document(
                    m.chat.id,
                    document=file["file_id"],
                    caption=file.get("caption", "")
                )
            except Exception as e:
                print(f"[send_file error] {file.get('file_name', 'Unknown')} – {e}")
    except Exception as e:
        await m.reply_text("❌ Failed to complete the sequence.")
        print(f"[endsequence error] {e}")

# ─────────────────────────────────────────────
# /showsequence – Show all collected files
# ─────────────────────────────────────────────
@Client.on_message(filters.private & filters.command("showsequence"))
async def show_sequence(c: Client, m: Message):
    """
    Lists all files currently added to the user's sequence.
    """
    try:
        files = await Element_Network.get_sequence(m.from_user.id)

        if not files:
            return await m.reply_text("📭 You haven’t added any files to the sequence.")

        text = "<b>📋 Files in current sequence:</b>\n\n"
        for i, f in enumerate(files, 1):
            text += f"{i}. {f.get('file_name', 'Unnamed')}\n"

        await m.reply_text(text, parse_mode="html")
    except Exception as e:
        await m.reply_text("⚠️ Couldn’t retrieve your sequence.")
        print(f"[showsequence error] {e}")

# ─────────────────────────────────────────────
# /cancelsequence – Wipe stored file sequence
# ─────────────────────────────────────────────
@Client.on_message(filters.private & filters.command("cancelsequence"))
async def cancel_sequence(c: Client, m: Message):
    """
    Cancels the sequence session and clears any stored files.
    """
    try:
        await Element_Network.cancel_sequence(m.from_user.id)
        await m.reply_text("🗑️ Sequence cancelled. No files saved.")
    except Exception as e:
        await m.reply_text("⚠️ Couldn't cancel your sequence.")
        print(f"[cancelsequence error] {e}")
        

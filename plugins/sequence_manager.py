from pyrogram import Client, filters
from pyrogram.types import Message
from helper.database import Element_Network


@Client.on_message(filters.private & filters.command("startsequence"))
async def start_sequence(c: Client, m: Message):
    """
    Starts a new renaming sequence for the user.
    """
    try:
        await Element_Network.start_sequence(m.from_user.id)
        await m.reply_text("🔄 Sequence mode started.\n\nNow send your files one at a time.")
    except Exception as e:
        await m.reply_text("❌ Failed to start sequence.")
        print(f"[startsequence error] {e}")


@Client.on_message(filters.private & filters.command("endsequence"))
async def end_sequence(c: Client, m: Message):
    """
    Ends the sequence and sends all collected files back to the user.
    """
    try:
        files = await Element_Network.end_sequence(m.from_user.id)

        if not files:
            return await m.reply_text("ℹ️ Sequence is empty. Nothing to send.")

        await m.reply_text("📦 Sending your sorted and renamed files...")

        for file in files:
            try:
                await c.send_document(
                    m.chat.id,
                    document=file["file_id"],
                    caption=file.get("caption", "")
                )
            except Exception as e:
                print(f"[send_file error] {file['file_name']} – {e}")

    except Exception as e:
        await m.reply_text("❌ Failed to complete the sequence.")
        print(f"[endsequence error] {e}")


@Client.on_message(filters.private & filters.command("showsequence"))
async def show_sequence(c: Client, m: Message):
    """
    Lists all files currently stored in the user's sequence.
    """
    try:
        files = await Element_Network.get_sequence(m.from_user.id)

        if not files:
            return await m.reply_text("📭 You haven’t added any files to the sequence yet.")

        text = "\n".join([f"{i+1}. {f['file_name']}" for i, f in enumerate(files)])
        await m.reply_text(f"📋 Files in sequence:\n\n{text}")
    except Exception as e:
        await m.reply_text("⚠️ Unable to list sequence files.")
        print(f"[showsequence error] {e}")


@Client.on_message(filters.private & filters.command("cancelsequence"))
async def cancel_sequence(c: Client, m: Message):
    """
    Cancels and clears the sequence from the database.
    """
    try:
        await Element_Network.cancel_sequence(m.from_user.id)
        await m.reply_text("❌ Sequence cancelled. No files saved.")
    except Exception as e:
        await m.reply_text("⚠️ Couldn't cancel sequence.")
        print(f"[cancelsequence error] {e}")



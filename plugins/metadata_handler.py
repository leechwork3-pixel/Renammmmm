from pyrogram import Client, filters
from pyrogram.types import Message
from helper.database import Element_Network

# ─────────────────────────────────────────────
# Toggle metadata embedding
# ─────────────────────────────────────────────
@Client.on_message(filters.private & filters.command("metadata"))
async def toggle_metadata(c: Client, m: Message):
    """
    Toggle metadata embedding on/off for the user.
    """
    try:
        status = await Element_Network.toggle_metadata(m.from_user.id)
        await m.reply_text(
            f"🛠 Metadata **{'ENABLED' if status else 'DISABLED'}** for your files.\n\n"
            f"Use commands like `/settitle`, `/setseason`, `/setepisode` to set values."
        )
    except Exception as e:
        await m.reply_text("❌ Could not toggle metadata embedding.")
        print(f"[toggle_metadata error] {e}")

# ─────────────────────────────────────────────
# Set metadata field
# ─────────────────────────────────────────────
@Client.on_message(filters.private & filters.command([
    "settitle", "setauthor", "setartist", "setaudio", "setsubtitle", "setvideo",
    "setseason", "setepisode", "setchapter", "setquality", "setlanguage",
    "setresolution", "setyear", "setcustom"
]))
async def set_metadata_field(c: Client, m: Message):
    """
    Sets a specific metadata field for the user.
    Usage: /settitle My Title
    """
    try:
        if len(m.command) < 2:
            return await m.reply_text("❗ Send something after the command.")

        value = m.text.split(" ", 1)[1].strip()
        if not value:
            return await m.reply_text("❗ Value cannot be empty.")

        # Field name is command without 'set'
        cmd = m.command[0].lower()[3:]  # 'settitle' -> 'title'
        await Element_Network.set_metadata(m.from_user.id, cmd, value)
        await m.reply_text(f"✅ Set `{cmd}` to:\n\n`{value}`")
    except Exception as e:
        await m.reply_text("❌ Failed to set metadata field.")
        print(f"[set_metadata_field error] {e}")

# ─────────────────────────────────────────────
# Remove metadata field
# ─────────────────────────────────────────────
@Client.on_message(filters.private & filters.command("removemetadata"))
async def remove_metadata_field(c: Client, m: Message):
    """
    Removes a specific metadata field by setting it to empty.
    Usage: /removemetadata season
    """
    try:
        if len(m.command) < 2:
            return await m.reply_text("❗ Please specify which metadata field to remove.")

        field = m.command[1].lower()
        valid_fields = {
            "title", "author", "artist", "audio", "subtitle", "video",
            "season", "episode", "chapter", "quality", "language",
            "resolution", "year", "custom"
        }

        if field not in valid_fields:
            return await m.reply_text(f"❗ Invalid field name: `{field}`")

        await Element_Network.set_metadata(m.from_user.id, field, "")
        await m.reply_text(f"✅ Removed metadata field `{field}`.")
    except Exception as e:
        await m.reply_text("❌ Failed to remove metadata field.")
        print(f"[remove_metadata_field error] {e}")
        

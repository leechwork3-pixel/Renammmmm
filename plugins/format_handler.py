from pyrogram import Client, filters
from pyrogram.types import Message
from helper.database import Element_Network

@Client.on_message(filters.private & filters.command("format"))
async def show_format_help(client: Client, message: Message):
    """
    Show available placeholders and current rename format template.
    """
    user_id = message.from_user.id
    current_template = await Element_Network.get_format_template(user_id) or "{filename}{ext}"
    text = (
        "**📝 Rename Format Help**\n\n"
        "You can use the following placeholders in your file name template:\n\n"
        "`{filename}` – original name (no extension)\n"
        "`{ext}` – original extension\n"
        "`{season}` `{episode}` `{chapter}` `{resolution}` `{quality}`\n"
        "`{language}` `{year}` `{title}` `{custom}`\n\n"
        "➡️ Example:\n`/setformat {title}.S{season}E{episode}.{quality}{ext}`\n\n"
        f"📌 Your current format:\n`{current_template}`"
    )
    await message.reply_text(text, parse_mode="markdown")

@Client.on_message(filters.private & filters.command("setformat"))
async def set_format_template(client: Client, message: Message):
    """
    Lets the user set a custom rename format template.
    """
    user_id = message.from_user.id
    if len(message.command) < 2:
        return await message.reply_text("❗ Usage: `/setformat <template>`", parse_mode="markdown")

    template = message.text.split(" ", 1)[1]
    await Element_Network.set_format_template(user_id, template)
    await message.reply_text("✅ Format template saved.")


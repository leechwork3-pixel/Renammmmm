import os


class Config:
    API_ID = int(os.environ.get("API_ID", 123456))
    API_HASH = os.environ.get("API_HASH", "your_api_hash")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_bot_token")

    DB_URL = os.environ.get("DB_URL", "mongodb+srv://...")
    DB_NAME = os.environ.get("DB_NAME", "AutoRenameBot")

    START_PIC = os.environ.get("START_PIC", "https://te.legra.ph/file/45453c9242ee37aa1670d.jpg")
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1001234567890"))
    SUPPORT_CHAT = int(os.environ.get("SUPPORT_CHAT", "-1001234567890"))

    PORT = int(os.environ.get("PORT", 8080))
    BOT_OWNER = int(os.environ.get("BOT_OWNER", "123456789"))

    WEBHOOK = os.environ.get("WEBHOOK", "False").lower() == "true"

    FORCE_SUB_CHANNELS = os.environ.get("FORCE_SUB_CHANNELS", "").split(',')

    BOT_UPTIME = os.environ.get("BOT_UPTIME", "Unknown")


class Txt:
    START_TXT = """**👋 Hello! I'm AutoRenameBot**  
I can help you rename Telegram files with your desired formatting.  
Set your template using `/format <template>` or `/setformat <template>`.  
Enjoy a fast and flexible renaming experience.

👮 Powered by: @Shadow_Blank"""

    HELP_TXT = """**🛠 How to Use Me:**

/format or /setformat – Set the rename format  
/metadata – Toggle metadata editor (title, author, etc.)  
/startsequence – Begin sequence renaming  
/endsequence – Finish & sort sequence  
/myplan – Check premium status  
/settitle, /setauthor, /setartist... – Set metadata fields
/view_thumb – See current thumbnail  
/set_caption – Add custom caption  
/del_caption – Remove saved caption

✨ Premium users get better speeds and more features!
"""

    ABOUT_TXT = """🤖 **Bot Version:** AutoRenameBot v3.1  
🧑‍💻 **Developer:** @Shadow_Blank  
🗃️ **Library:** [Pyrogram](https://github.com/pyrogram/pyrogram)  
📡 **Hosted on:** Koyeb / Render Compatible"""

    FILE_NAME_TXT = """**📁 File Formatting Help:**

You can use these placeholders:
• {filename} = original name  
• {ext} = extension (e.g. .mp4)  
• {quality}, {season}, {episode} = manual values

👉 Example:
/format Series S{season}E{episode} [{quality}]{ext}
"""

    DONATE_TXT = """**💸 Support Development**

If you enjoy using this bot, consider donating:

🟢 UPI: `Shadow_Blank@ybl`  
📩 Send screenshot to @Shadow_Blank
"""

    PLAN_TEXT = """**💠 Premium Plans – Unlock More Power**

• 1 Month – ₹40  
• 2 Months – ₹70  
• 4 Months – ₹130  

Pay via UPI: `Shadow_Blank@ybl`  
Then DM proof to @Shadow_Blank"""

    META_TXT = """📽️ **Metadata Selection Instructions**

Set custom strings to embed as title/author/artist/audio/subtitle/video.

Use:
/settitle  
/setauthor  
/setartist  
/setvideo  

Use `/metadata` to toggle embedding support."""

    PROGRESS_BAR = """

📊 {0}% Done  
⏱ {3}/s | 📦 {1}/{2} | ⏳ ETA: {4}"""
  

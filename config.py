import os
import re
import time

# Match numeric IDs (for casting from env)
id_pattern = re.compile(r'^-?\d+$')

class Config:
    # ---- Pyrogram / Bot credentials ----
    API_ID = int(os.environ.get("API_ID", 123456))
    API_HASH = os.environ.get("API_HASH", "your_api_hash")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_bot_token")

    # ---- Database ----
    DB_URL = os.environ.get("DB_URL", "mongodb://localhost:27017")
    DB_NAME = os.environ.get("DB_NAME", "AutoRenameBot")

    # ---- Channels ----
    START_PIC = os.environ.get(
        "START_PIC",
        "https://te.legra.ph/file/45453c9242ee37aa1670d.jpg"
    )
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1001234567890"))
    SUPPORT_CHAT = int(os.environ.get("SUPPORT_CHAT", "-1001234567890"))

    # Force subscribe channels (comma-separated)
    FORCE_SUB_CHANNELS = [
        int(x) if id_pattern.match(x) else x
        for x in os.environ.get("FORCE_SUB_CHANNELS", "").split(',') if x
    ]

    # ---- Owner/Admin ----
    BOT_OWNER = int(os.environ.get("BOT_OWNER", "123456789"))

    # ---- Hosting/Webhook ----
    PORT = int(os.environ.get("PORT", 8080))
    WEBHOOK = os.environ.get("WEBHOOK", "False").lower() == "true"

    # ---- Alias for backward compatibility ----
    DUMP_CHANNEL = int(os.environ.get("DUMP_CHANNEL", "-1002887783820"))
    STORAGE_CHANNEL = DUMP_CHANNEL

    # ---- Uptime ----
    BOT_UPTIME = time.time()


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
• {filename} = original name (no extension)  
• {ext} = file extension (e.g. .mp4)  
• {quality} = quality tag  
• {season} = season number  
• {episode} = episode number  
• {chapter} = chapter number  
• {language} = language code or label  
• {resolution} = resolution (e.g. 1080p)  
• {year} = release year  
• {custom} = custom user text

👉 Example:  
/format {title} S{season}E{episode} [{quality}]{ext}
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


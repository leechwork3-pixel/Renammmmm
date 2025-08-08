import os
import re
import time

# Pattern to validate integer values like chat IDs
id_pattern = re.compile(r'^-?\d+$')


class Config:
    # ────────── Bot Authentication ──────────
    API_ID = int(os.environ.get("API_ID", "123456"))
    API_HASH = os.environ.get("API_HASH", "your_api_hash")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_bot_token")
    BOT_USERNAME = os.environ.get("BOT_USERNAME", "AutoRenameBot")

    # ────────── MongoDB Database ──────────
    DB_URL = os.environ.get("DB_URL", "mongodb://localhost:27017")
    DB_NAME = os.environ.get("DB_NAME", "AutoRenameBot")

    # ────────── Channels / Alerts ──────────
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1001234567890"))
    SUPPORT_CHAT = int(os.environ.get("SUPPORT_CHAT", "-1001234567890"))
    DUMP_CHANNEL = int(os.environ.get("DUMP_CHANNEL", "-1002887783820"))
    STORAGE_CHANNEL = DUMP_CHANNEL

    FORCE_SUB_CHANNELS = [
        int(x) if id_pattern.match(x) else x
        for x in os.environ.get("FORCE_SUB_CHANNELS", "").split(',') if x
    ]

    START_PIC = os.environ.get(
        "START_PIC",
        "https://te.legra.ph/file/45453c9242ee37aa1670d.jpg"
    )

    # ────────── Owner/Admin Control ──────────
    BOT_OWNER = int(os.environ.get("BOT_OWNER", "123456789"))
    ADMIN = [BOT_OWNER]  # You can add more user IDs here manually if needed

    # ────────── Webhook/Hosting ──────────
    PORT = int(os.environ.get("PORT", 8080))
    WEBHOOK = os.environ.get("WEBHOOK", "False").lower() in ["true", "1"]

    # ────────── Runtime Info ──────────
    BOT_UPTIME = time.time()


class Txt:
    START_TXT = """**👋 Hello! I'm AutoRenameBot**  

I help you rename Telegram files with custom formatting, metadata, thumbnails, and more.  

Use /format or /setformat to set your rename pattern. Start uploading and renaming instantly!

👨‍💻 Powered by: @Shadow_Blank"""

    HELP_TXT = """**🛠 How to Use Me:**  
Rename, customize and format like a pro.

🔹 /format • /setformat – Set rename format  
🔹 /metadata – Toggle metadata embedding  
🔹 /startsequence – Start multi-file sequence  
🔹 /endsequence – Finalize & send sequence  
🔹 /myplan – Shows premium status  
🔹 /settitle, /setseason, /setlanguage, etc – Metadata fields  
🔹 /set_caption – Caption template  
🔹 /view_thumb – View thumbnail  
🔹 /del_caption – Remove saved caption  

🚀 Premium users enjoy higher speed & more features.
"""

    ABOUT_TXT = """**ℹ️ Bot Info**

🤖 Bot Name: AutoRenameBot  
👨‍💻 Dev: @Shadow_Blank  
📚 Library: Pyrogram v2  
🧠 Language: Python 3  
☁️ Hosting: VPS / Koyeb / Render

🔗 Source: Contact developer"""

    FILE_NAME_TXT = """**🔡 Rename Format Placeholders:**  

Use these variables in /format or /setformat:

• {filename} – Original filename (no ext)  
• {ext} – File extension  
• {title}, {quality}, {language}, {resolution}  
• {season}, {episode}, {chapter}  
• {year}, {custom}

📝 Example:  
`/setformat {title}.S{season}E{episode}.{quality}{ext}`"""

    DONATE_TXT = """**💰 Donations Welcome**

If this bot helped you, consider donating:

✅ UPI: `Shadow_Blank@ybl`  
📩 Send receipt to @Shadow_Blank

Thanks for supporting free tools ❤️"""

    PLAN_TEXT = """**💠 Premium Plans**

Access more speed & file capacity:

• 1 Month – ₹40  
• 2 Months – ₹70  
• Lifetime – ₹200

Pay via UPI: `Shadow_Blank@ybl`  
Then message @Shadow_Blank with your Telegram ID.
"""

    META_TXT = """🎞️ **Metadata Help**

Insert embedded metadata into files using:

/settitle <name>  
/setauthor <text>  
/setartist <text>  
/setvideo <text>  
/removefield <metadata_key>  
/metadata to toggle on/off

Supports most MP4, MKV and audio formats."""

    SEQUENCE_TXT = """📁 **Sequence Rename Help**

Sequence mode lets you queue multiple files and rename them all at once.

1. Send `/startsequence`  
2. Upload files one by one  
3. Send `/endsequence` to receive them renamed  
4. `/cancelsequence` to discard session"""

    THUMBNAIL_TXT = """🖼 **Thumbnail Management**

• Send a photo with caption `/set_thumb` to save thumbnail  
• `/view_thumb` to preview thumbnail  
• `/del_thumb` to reset thumbnail"""

    CAPTION_TXT = """✏️ **Custom Caption**

Use variables in your caption:

• `{filename}` – File name  
• `{filesize}` – File size  
• `{duration}` – Duration (for video/audio)

✅ Example:  
`/set_caption {filename} | {filesize}`

You can delete using `/del_caption` or preview with `/view_caption`.
"""

    SOURCE_TXT = """🧪 This bot is custom-built by @Shadow_Blank.

For deployment/custom version, contact the dev."""
    
    PREMIUM_TXT = PLAN_TEXT
    PROGRESS_BAR = """

📊 {0}%  
📦 {1}/{2} | ⚡ {3}/s  
⏳ ETA: {4}"""

import os
import re
import time

# Pattern to validate integer values like chat or user IDs
id_pattern = re.compile(r'^-?\d+$')


class Config:
    # ────────── Bot Authentication ──────────
    API_ID = int(os.environ.get("API_ID", "24171111"))
    API_HASH = os.environ.get("API_HASH", "c850cb56b64b6c3b10ade9c28ef7966a")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "7813615574:AAFiXEgYhwsu1xs0RN5aRVUAFgoUq32NzbU")
    BOT_USERNAME = os.environ.get("BOT_USERNAME", "AutoRenamerr_Bot")

    # ────────── MongoDB Database ──────────
    DB_URL = os.environ.get("DB_URL", "mongodb+srv://Furina:furinafile@furinafile.tjrqfwh.mongodb.net/?retryWrites=true&w=majority&appName=Furinafile")
    DB_NAME = os.environ.get("DB_NAME", "AutoRenameBot")

    # ────────── Channels / Notifications ──────────
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1002104276255"))
    SUPPORT_CHAT = int(os.environ.get("SUPPORT_CHAT", "-1002329676743"))
    DUMP_CHANNEL = int(os.environ.get("DUMP_CHANNEL", "-1002104276255"))
    STORAGE_CHANNEL = DUMP_CHANNEL

    FORCE_SUB_CHANNELS = [
        int(x) if id_pattern.match(x) else x
        for x in os.environ.get("FORCE_SUB_CHANNELS", "-1002851018823").split(",") if x
    ]

    # ────────── Bot Ownership / Admin List ──────────
    BOT_OWNER = int(os.environ.get("BOT_OWNER", "1335306418"))
    ADMIN = list(set(
        [BOT_OWNER] + [
            int(x) if id_pattern.match(x) else x
            for x in os.environ.get("ADMIN", "1335306418").split()
            if x
        ]
    ))

    # ────────── Hosting & Webhook Settings ──────────
    WEBHOOK = os.environ.get("WEBHOOK", "False").lower() in ["true", "1"]
    PORT = int(os.environ.get("PORT", 8080))

    # ────────── Display Assets ──────────
    START_PIC = os.environ.get(
        "START_PIC", "https://te.legra.ph/file/45453c9242ee37aa1670d.jpg"
    )

    # ────────── Runtime State ──────────
    BOT_UPTIME = time.time()
    DOWNLOAD_DIR = os.environ.get("DOWNLOAD_DIR", "downloads")
    METADATA_DIR = os.environ.get("METADATA_DIR", "metadata")

    # ────────── Rename Formatting Defaults ──────────
    DEFAULT_RENAME_PATTERN = os.environ.get("DEFAULT_RENAME_PATTERN", "{filename}")
    CAPTION_PLACEHOLDER = os.environ.get("CAPTION_PLACEHOLDER", "{filename} | {filesize}")

    # ────────── Optional Metadata Defaults ──────────
    TITLE = os.environ.get("TITLE", "")
    AUTHOR = os.environ.get("AUTHOR", "")
    ARTIST = os.environ.get("ARTIST", "")
    CHAPTER = os.environ.get("CHAPTER", "")
    YEAR = os.environ.get("YEAR", "")
    SEASON = os.environ.get("SEASON", "")
    EPISODE = os.environ.get("EPISODE", "")
    QUALITY = os.environ.get("QUALITY", "WEB-DL")
    LANGUAGE = os.environ.get("LANGUAGE", "English")
    RESOLUTION = os.environ.get("RESOLUTION", "1080p")
    CUSTOM_TEXT = os.environ.get("CUSTOM_TEXT", "")

    # ────────── Feature Flags ──────────
    CLEANUP = os.environ.get("CLEANUP", "True").lower() in ["true", "1"]
    DELETE_MSG = os.environ.get("DELETE_MSG", "False").lower() in ["true", "1"]
    ENABLE_PREMIUM = os.environ.get("ENABLE_PREMIUM", "False").lower() in ["true", "1"]
    BROADCAST = os.environ.get("BROADCAST", "True").lower() in ["true", "1"]
    PREMIUM_TAG = os.environ.get("PREMIUM_TAG", "💎")

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

🚀 Premium users enjoy higher speed & more features."""

    ABOUT_TXT = """**ℹ️ Bot Info**

🤖 Bot: AutoRenameBot  
👨‍💻 Developer: @Shadow_Blank  
📚 Library: Pyrogram v2  
💻 Language: Python 3  
☁️ Hosting: VPS / Koyeb / Render

🔗 Source code available via developer."""

    FILE_NAME_TXT = """**🔡 Rename Format Placeholders:**  

You can use these in /format or /setformat:

• {filename} → Original name  
• {ext} → Extension  
• {title}, {season}, {episode}, {quality}  
• {language}, {resolution}, {year}, {custom}

📝 Example:  
`/setformat {title}.S{season}E{episode}.{quality}{ext}`"""

    DONATE_TXT = """**💰 Donations Welcome**

☕ If this bot helps you, consider supporting:

✅ UPI: `Shadow_Blank@ybl`  
📩 Send receipt to @Shadow_Blank

Thanks for supporting free tools ❤️"""

    PLAN_TEXT = """**💠 Premium Plans**

Unlock more speed, size, and priority:

• 1 Month – ₹40  
• 2 Months – ₹70  
• Lifetime – ₹200

💸 Pay via UPI: `Shadow_Blank@ybl`  
➤ Then DM @Shadow_Blank with proof & @ID"""

    META_TXT = """🎞️ **Metadata Help**

Update embedded tags using:

/settitle, /setartist, /setauthor  
/setvideo, /setaudio, /setsubtitle  
/removefield <key>

/metadata – Toggle metadata on/off"""

    SEQUENCE_TXT = """📁 **Sequence Rename**

1. `/startsequence` – Begin upload session  
2. Upload files one by one  
3. `/endsequence` – Get renamed set  
💡 Useful for TV series, batches, etc."""

    THUMBNAIL_TXT = """🖼 **Thumbnail & Poster**

• Send photo with `/set_thumb`  
• `/view_thumb` → Preview current one  
• `/del_thumb` → Reset thumbnail"""

    CAPTION_TXT = """✏️ **Custom Caption Format**

Use in `/set_caption`:

• {filename}  
• {filesize}  
• {duration}

Example:  
`{filename} | {filesize}`"""

    SOURCE_TXT = """🧪 *Open Source Notice*

This bot is a custom build for media enthusiasts.

To deploy or get a paid version → Contact @Shadow_Blank."""

    PREMIUM_TXT = PLAN_TEXT

    PROGRESS_BAR = """
📊 {0}%  
📦 {1}/{2} | ⚡ {3}/s  
⏳ ETA: {4}"""
    

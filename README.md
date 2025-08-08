# 🛠️ AutoRenameBot

A powerful Telegram bot to rename, retitle, and reformat your Telegram media — fast, customizable, and fully async.

---

## ✨ Features

- Rename files via templates (e.g. `/format Series S{season}E{episode}`)
- Set custom thumbnails and captions
- Edit metadata: title, author, artist, etc.
- Sequence renaming (sort episodes automatically)
- NSFW filtering (filename/content block)
- Premium mode support
- Force subscription / logging channels
- Webhook or polling support (Render / Koyeb / VPS)

---

## 🚀 Deployment

### 🔧 Environment Variables Required

| Variable         | Description                                   |
|------------------|-----------------------------------------------|
| `API_ID`         | From my.telegram.org                          |
| `API_HASH`       | From my.telegram.org                          |
| `BOT_TOKEN`      | Your BotFather token                          |
| `DB_URL`         | MongoDB URI                                   |
| `DB_NAME`        | MongoDB database name                         |
| `LOG_CHANNEL`    | Log group ID (including `-100`)               |
| `SUPPORT_CHAT`   | Support group or channel ID                   |
| `WEBHOOK`        | `True` for Render/Koyeb, `False` for polling  |
| `START_PIC`      | URL for start banner (optional)               |
| `BOT_OWNER`      | Your user ID                                  |
| `FORCE_SUB_CHANNELS` | Channel usernames IDs separated by `,`    |

---

### 🐳 Docker Deploy

git clone https://github.com/yourrepo/AutoRenameBot
cd AutoRenameBot
docker build -t autorename .
docker run --env-file .env autorename

📝 Use a `.env` file to define secrets like:

BOT_TOKEN=your_bot_token
API_ID=1111111
API_HASH=yourapihash
...

---

## 🧰 Commands Reference

### 👥 User Commands

/start – Bot welcome
/format [template] – Set rename format
/setformat [template] – Alias of /format
/startsequence – Begin sorting
/endsequence – Send final sorted batch
/set_caption, /view_thumb – Caption/thumb tools
/myplan – See premium status


### 🔐 Admin/Owner Commands

/restart – Force restart
/status – Show stats
/addpremium [user] [days]
/rmpremium [user]


---

## 👤 Credits

- Developer: [@Shadow_Blank](https://t.me/Shadow_Blank)  
- Inspired by: Codeflix-Bots / Pyrogram Community  
- Database Engine: Element_Network (MongoDB wrapper)

---

## 📌 License

© 2025 Shadow_Blank. Licensed under GPLv3.



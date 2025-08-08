# 🤖 AutoRenameBot

A powerful and feature-rich Telegram Bot that helps you rename & format files with thumbnails, captions, metadata, and more — powered by Pyrogram.

Supports documents, audio, video, and batch rename operations with premium features and admin controls 🎛

---

## 🚀 Features

- ✅ Rename Telegram files (video, audio, document)
- 🎯 Set formatting templates with placeholders
- 📝 Custom thumbnails & captions
- 🧾 Embed metadata (title, quality, episode, etc.)
- 🧵 Sequence/bulk renaming
- 💎 Premium user system
- 🔒 Force join channels before bot usage
- 📢 Broadcast & Admin commands
- 💨 Koyeb / Render / Docker deployable

---

## 🌐 Environment Variables (.env)

| Key                  | Required | Description                                      |
|----------------------|----------|--------------------------------------------------|
| API_ID               | ✅       | Telegram API ID                                  |
| API_HASH             | ✅       | Telegram API Hash                                |
| BOT_TOKEN            | ✅       | Token from @BotFather                            |
| DB_URL               | ✅       | MongoDB connection string (MongoDB Atlas/local)  |
| DB_NAME              | ❌       | MongoDB database name (default: AutoRenameBot)   |
| LOG_CHANNEL          | ✅       | Channel ID for status updates                    |
| SUPPORT_CHAT         | ❌       | Group/channel to link as contact/help            |
| DUMP_CHANNEL         | ✅       | Storage channel ID for renamed file logs         |
| BOT_OWNER            | ✅       | Your own Telegram user ID                        |
| START_PIC            | ❌       | Image URL for /start message                     |
| FORCE_SUB_CHANNELS   | ❌       | Comma-separated list of @channels or -100 IDs    |
| PORT                 | ❌       | Webhook port (default: 8080)                     |
| WEBHOOK              | ❌       | Use webhook (True/False)                         |

---

## 📦 Installation

git clone https://github.com/yourusername/AutoRenameBot
cd AutoRenameBot
pip install -r requirements.txt

cp .env.example .env

Fill your credentials in the .env file
python bot.py

---

## 🐳 Docker Deployment

docker build -t autorenamebot .
docker run --env-file .env autorenamebot

Or deploy using DockerHub + Koyeb with the included `koyeb.yaml`.

---

## 📚 Bot Commands

### 🧩 General

| Command     | Function                                 |
|-------------|-------------------------------------------|
| /start      | Start the bot                            |
| /help       | Show help menu                           |
| /about      | Show about the bot                       |
| /tutorial   | Format guide and placeholders            |

### ✏️ Rename & Template

| Command              | Function                                         |
|----------------------|--------------------------------------------------|
| /setformat <format>  | Set static rename template                       |
| /format              | View available placeholders                      |
| /autorename <format> | (Premium) Quick rename formatting                |
| /setmedia            | (Premium) Choose output: document, video, audio  |

🧩 Available placeholders: `{title}`, `{quality}`, `{season}`, `{episode}`, `{language}`, `{ext}`, `{custom}`

### 🖼️ Captions & Thumbnails

| Command         | Purpose                              |
|------------------|---------------------------------------|
| /set_caption     | Save a caption with variables         |
| /view_caption    | View saved caption                    |
| /del_caption     | Delete saved caption                  |
| /set_thumb       | Send thumb image + use this command   |
| /view_thumb      | Show current thumbnail                |
| /del_thumb       | Delete saved thumbnail                |

### 🎞 Metadata Editor

| Command           | Description                       |
|--------------------|-----------------------------------|
| /metadata          | Toggle metadata usage             |
| /settitle, /setauthor, /setquality etc. | Set tags    |
| /removemetadata    | Clear specific metadata field     |

### 🧵 Queue & Sequence

| Command             | Description                        |
|----------------------|------------------------------------|
| /startsequence       | Start batching files               |
| /endsequence         | Stop sequence and rename them      |
| /showsequence        | Show queued sequence list          |
| /cancelsequence      | Cancel active sequence mode        |
| /queue               | See user's file processing queue   |
| /clearqueue          | Clear user's rename queue          |
| /removefromqueue     | Remove a file from your queue      |
| /clearallqueue       | (Admin) Remove queues for all users|

### 💎 Premium Access

| Command               | Description                    |
|------------------------|--------------------------------|
| /myplan               | View your premium status       |
| /addpremium <id> <days> | (Admin) Add premium days     |
| /rmpremium <id>       | (Admin) Remove premium access  |
| /premiumusers         | (Admin) List all premium users |

### 👑 Admin Tools

| Command             | Purpose                               |
|----------------------|----------------------------------------|
| /broadcast (reply) | Send to all users (reply-based)        |
| /restart            | Restart the bot                       |
| /stats /status      | View bot uptime and user count         |
| /ban, /unban        | Block/unblock user interaction         |
| /leaderboard        | Top active users                       |
| /search <keyword>   | Search dumped files via caption        |

---

## 🔒 Force Subscribe

If enabled via `FORCE_SUB_CHANNELS`, users must join your update channels before they can use the bot.

They’ll see inline toggle and invite buttons until all conditions are met.

---

## 🧑‍💻 Credits

- 🧠 Developed & maintained by: [@Shadow_Blank](https://t.me/Shadow_Blank)
- ⚙️ Powered by: Python 3.10 · Pyrogram 2.x · MongoDB
- ☁️ Deployment: Koyeb, Render, Heroku (Docker)

---

## 📄 License

MIT License  
Feel free to use, fork, deploy — stars welcome ⭐


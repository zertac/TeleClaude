<p align="center">
  <img src="logo.png" alt="TeleClaude Logo" width="150">
</p>

<h1 align="center">TeleClaude</h1>

<p align="center">
  <strong>Control Claude AI from anywhere via Telegram</strong>
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-requirements">Requirements</a> •
  <a href="#-installation">Installation</a> •
  <a href="#-usage">Usage</a> •
  <a href="#-bot-commands">Commands</a> •
  <a href="#-roadmap">Roadmap</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Windows-blue?logo=windows" alt="Windows">
  <img src="https://img.shields.io/badge/Python-3.10+-green?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Claude-CLI-orange?logo=anthropic" alt="Claude CLI">
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="License">
</p>

---

## 🤔 What is TeleClaude?

TeleClaude is a Windows bot that connects **Telegram** with **Claude CLI**. Send a message from your phone, and Claude AI will respond — just like chatting with a friend, but it's an AI assistant that can:

- 💻 Write and edit code on your computer
- 📁 Read and manage files
- 🔧 Run commands and scripts
- 🧠 Remember your conversation context

**Perfect for:** Developers who want to control their dev environment remotely, run Claude tasks while away from their PC, or just chat with Claude on the go.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔄 **Conversation Memory** | Claude remembers previous messages in the session |
| 📂 **Remote File Access** | Download files from your PC via Telegram |
| 📍 **Working Directory** | Change Claude's working folder on the fly |
| 🔁 **Auto-Restart** | Bot automatically recovers from crashes |
| 🚀 **Windows Startup** | One-click setup to run on boot |
| 🔒 **Access Control** | Restrict bot to your Telegram ID only |

---

## 📋 Requirements

Before installing TeleClaude, make sure you have:

| Requirement | How to Get |
|-------------|------------|
| **Windows 10/11** | You probably have this already |
| **Python 3.10+** | [Download Python](https://www.python.org/downloads/) — Check "Add to PATH" during install! |
| **Claude CLI** | [Install Claude CLI](https://github.com/anthropics/claude-code) — Must be accessible via `claude` command |
| **Telegram Bot Token** | Create one with [@BotFather](https://t.me/botfather) (instructions below) |

### 🤖 Getting Your Telegram Bot Token

1. Open Telegram and search for **@BotFather**
2. Send `/newbot` command
3. Choose a **name** for your bot (e.g., "My Claude Bot")
4. Choose a **username** (must end with `bot`, e.g., `my_claude_bot`)
5. BotFather will give you a **token** like: `123456789:ABCdefGHI...`
6. **Save this token** — you'll need it during setup!

> ⚠️ **Keep your token secret!** Anyone with it can control your bot.

---

## 🚀 Installation

### Step 1: Clone the Repository

```cmd
git clone https://github.com/zertach/TeleClaude.git
cd TeleClaude
```

### Step 2: Install Python Package

```cmd
pip install -r requirements.txt
```

This installs `python-telegram-bot` library.

### Step 3: Configure the Bot

Open `config.json` in any text editor (Notepad works fine):

```json
{
  "telegram_bot_token": "YOUR_BOT_TOKEN_HERE",
  "allowed_user_ids": [],
  "working_dir": ""
}
```

| Field | What to Put |
|-------|-------------|
| `telegram_bot_token` | Paste your token from BotFather |
| `allowed_user_ids` | Your Telegram ID (get it by running the bot and sending `/start`) |
| `working_dir` | Folder where Claude works (leave empty for bot's folder) |

**Example with values:**
```json
{
  "telegram_bot_token": "123456789:ABCdefGHIjklMNOpqrsTUVwxyz",
  "allowed_user_ids": [123456789],
  "working_dir": "C:\\Projects"
}
```

### Option B: Use Environment Variables

You can set environment variables instead of (or to override) `config.json`:

```cmd
set TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
set ALLOWED_USER_IDS=123456789,987654321
set WORKING_DIR=C:\Projects
```

- `ALLOWED_USER_IDS` accepts a comma/space-separated list or a JSON array (e.g., `[123456789]`).
- Environment variables override values from `config.json`.

### Step 4: Verify Claude CLI

Make sure Claude CLI is installed and working:

```cmd
claude --version
```

If this shows an error, [install Claude CLI](https://github.com/anthropics/claude-code) first.

### Step 5: Run the Bot

```cmd
bot_start.bat
```

🎉 **That's it!** Open Telegram, find your bot, and send a message!

---

## 💡 Usage

### ▶️ Starting the Bot

| Method | Command | Description |
|--------|---------|-------------|
| **Manual** | `bot_start.bat` | Run once, closes when you close the window |
| **Service** | `bot_service.bat` | Auto-restarts if it crashes |

### ⏹️ Stopping the Bot

```cmd
bot_stop.bat
```

### 🔄 Run on Windows Startup

Want the bot to start automatically when Windows boots?

```cmd
install_startup.bat
```

To remove from startup:

```cmd
uninstall_startup.bat
```

---

## 🎮 Bot Commands

Send these commands to your bot in Telegram:

| Command | Description |
|---------|-------------|
| `/start` | Shows your Telegram ID (use this for `allowed_user_ids`) |
| `/reset` | Starts a fresh conversation (clears context) |
| `/cd <path>` | Change Claude's working directory |
| `/pwd` | Show current working directory |
| `/getfile <path>` | Download a file to your phone (max 50MB) |

**Any other message** is sent directly to Claude AI.

### 📝 Example Conversation

```
You: Create a hello.py file that prints "Hello World"
Bot: I've created hello.py with the following content...

You: /getfile hello.py
Bot: 📎 hello.py

You: /cd C:\OtherProject
Bot: Working directory changed to: C:\OtherProject
```

---

## 🔒 Security

TeleClaude runs Claude with `--dangerously-skip-permissions` flag, which means **Claude has full access** to your system. This is required because there's no way to approve permissions via Telegram.

**Stay safe:**
- ✅ Always set your `allowed_user_ids`
- ✅ Keep your bot token private
- ✅ Limit `working_dir` to specific folders if needed
- ❌ Don't share your bot token with anyone

---

## 🛣️ Roadmap

Planned improvements for future versions:

- [ ] 🐧 Linux/macOS support
- [ ] 🖼️ Image support (send screenshots to Claude)
- [ ] 📊 Multi-user support with separate sessions
- [ ] ⚡ Webhook mode for faster responses
- [ ] 🔐 Optional permission approval via Telegram
- [ ] 📝 Conversation history logging
- [ ] 🌐 Web dashboard for monitoring

**Have ideas?** Open an issue or submit a PR!

---

## 🐛 Troubleshooting

### "Claude CLI not found"
Make sure you can run `claude --version` in Command Prompt. If not, [install Claude CLI](https://github.com/anthropics/claude-code) and restart your terminal.

### "python is not recognized"
Python isn't in your PATH. Reinstall Python and check **"Add Python to PATH"** during installation.

### Bot doesn't respond
1. Check if `bot_start.bat` window shows any errors
2. Verify your bot token is correct
3. Make sure your Telegram ID is in `allowed_user_ids` (or leave it empty to allow everyone)

### "Conflict: terminated by other getUpdates request"
Another instance of the bot is running. Run `bot_stop.bat` first, wait 30 seconds, then start again.

---

## 📄 License

MIT License — feel free to use, modify, and distribute.

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/zertach">zertach</a>
</p>

<p align="center">
  <a href="https://github.com/zertach/TeleClaude/issues">Report Bug</a> •
  <a href="https://github.com/zertach/TeleClaude/issues">Request Feature</a>
</p>

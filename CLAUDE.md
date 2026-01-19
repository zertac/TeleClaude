# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Telegram bot that bridges Telegram messaging with Claude CLI. Users send messages via Telegram, the bot forwards them to Claude CLI, and returns responses back through Telegram.

## Commands

### Running the Bot

```batch
bot_start.bat          # Manual start
bot_service.bat        # Service mode (auto-restart on crash)
bot_stop.bat           # Stop the bot
```

### Setup

```batch
pip install -r requirements.txt
# Edit config.json with your token
```

### Windows Startup

```batch
install_startup.bat    # Add to Windows startup
uninstall_startup.bat  # Remove from startup
```

## Architecture

Single-file Python application (`telegram_claude_bot.py`) with batch file wrappers.

**Flow:** Telegram Message -> Bot -> Claude CLI (subprocess with `--continue` flag) -> Response -> Telegram

**Configuration (`config.json`):**
- `telegram_bot_token` - Bot authentication token
- `allowed_user_ids` - Whitelist for access control (empty = allow all)
- `working_dir` - Default working directory (empty = script directory)

Claude CLI is auto-discovered from PATH using `shutil.which()`.

**Bot Commands:**
- `/start` - Shows user's Telegram ID
- `/reset` - Starts new conversation (skips `--continue` flag)
- `/cd [path]` - Changes working directory
- `/pwd` - Shows current working directory
- `/getfile [path]` - Downloads file via Telegram (50MB limit)

**Constraints:**
- 300 second timeout per Claude request
- Telegram message limit: 4096 chars (auto-split at 4000)
- Claude runs with `--dangerously-skip-permissions` flag

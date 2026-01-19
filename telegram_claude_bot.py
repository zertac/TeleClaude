import subprocess
import asyncio
import logging
import os
import json
import shutil
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ============ CONFIGURATION ============
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, "config.json")

def load_config():
    """Load configuration from config.json"""
    if not os.path.exists(CONFIG_FILE):
        print("=" * 50)
        print("ERROR: config.json not found!")
        print("=" * 50)
        print(f"\n1. Copy config.example.json to config.json")
        print(f"2. Add your Telegram bot token")
        print(f"3. (Optional) Add your Telegram ID to allowed_user_ids")
        print(f"\nFile location: {CONFIG_FILE}")
        return None

    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON format in config.json: {e}")
        return None

config = load_config()
if config is None:
    exit(1)

TELEGRAM_BOT_TOKEN = config.get("telegram_bot_token", "")
ALLOWED_USER_IDS = config.get("allowed_user_ids", [])
WORKING_DIR = config.get("working_dir", "") or SCRIPT_DIR

# Find Claude CLI from PATH
CLAUDE_CMD = shutil.which("claude")
if CLAUDE_CMD is None:
    # On Windows it might have .cmd extension
    CLAUDE_CMD = shutil.which("claude.cmd")

if CLAUDE_CMD is None:
    print("=" * 50)
    print("ERROR: Claude CLI not found!")
    print("=" * 50)
    print("\nMake sure Claude CLI is installed and added to PATH.")
    print("Check: claude --version")
    exit(1)
# ================================

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def run_claude(prompt: str, continue_conversation: bool = True) -> str:
    """Run Claude CLI and get response"""
    try:
        cmd = [CLAUDE_CMD]

        if continue_conversation:
            cmd.append("--continue")

        cmd.extend(["--dangerously-skip-permissions", "-p", prompt])

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,
            encoding='utf-8',
            errors='replace',
            cwd=WORKING_DIR
        )

        output = result.stdout.strip()

        if result.returncode != 0 and result.stderr:
            logger.warning(f"Claude stderr: {result.stderr}")
            if not output:
                output = f"Error: {result.stderr}"

        if not output:
            return "Empty response from Claude."

        return output

    except subprocess.TimeoutExpired:
        return "Timeout - Claude took too long (5 minute limit)."
    except FileNotFoundError:
        return "Error: Claude CLI not found. Is it in PATH?\nCheck: claude --version"
    except Exception as e:
        return f"Error: {str(e)}"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command - show user ID"""
    user = update.effective_user
    await update.message.reply_text(
        f"Hello {user.first_name}!\n\n"
        f"Your Telegram ID: {user.id}\n\n"
        f"Add this ID to config.json to restrict access to yourself only.\n\n"
        f"Send a message and I'll forward it to Claude."
    )

async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start a new conversation"""
    context.user_data['new_conversation'] = True
    await update.message.reply_text("Next message will start a new conversation.")

async def cd_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Change working directory"""
    global WORKING_DIR
    if context.args:
        new_dir = " ".join(context.args)
        if os.path.isdir(new_dir):
            WORKING_DIR = new_dir
            await update.message.reply_text(f"Working directory changed to: {WORKING_DIR}")
        else:
            await update.message.reply_text(f"Directory not found: {new_dir}")
    else:
        await update.message.reply_text(f"Current directory: {WORKING_DIR}\n\nUsage: /cd C:\\Projects")

async def pwd_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show current working directory"""
    await update.message.reply_text(f"Working directory: {WORKING_DIR}")

async def getfile_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a file"""
    if not context.args:
        await update.message.reply_text("Usage: /getfile file_path\nExample: /getfile C:\\Test\\bot.py")
        return

    file_path = " ".join(context.args)

    # If relative path, join with WORKING_DIR
    if not os.path.isabs(file_path):
        file_path = os.path.join(WORKING_DIR, file_path)

    if not os.path.exists(file_path):
        await update.message.reply_text(f"File not found: {file_path}")
        return

    if os.path.isdir(file_path):
        await update.message.reply_text(f"This is a directory, not a file: {file_path}")
        return

    try:
        # Check file size (Telegram limit ~50MB)
        size = os.path.getsize(file_path)
        if size > 50 * 1024 * 1024:
            await update.message.reply_text(f"File too large ({size // (1024*1024)} MB). Telegram limit is 50MB.")
            return

        await update.message.reply_document(document=open(file_path, 'rb'), filename=os.path.basename(file_path))
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming messages"""
    user_id = update.effective_user.id

    # Check user authorization
    if ALLOWED_USER_IDS and user_id not in ALLOWED_USER_IDS:
        await update.message.reply_text("You are not authorized to use this bot.")
        return

    user_message = update.message.text
    logger.info(f"User {user_id}: {user_message[:50]}...")

    # Show typing indicator
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    # Check if new conversation
    new_convo = context.user_data.get('new_conversation', False)
    if new_convo:
        context.user_data['new_conversation'] = False

    # Run Claude (blocking, so run in executor)
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, run_claude, user_message, not new_convo)

    # Telegram has 4096 char limit, split if needed
    if len(response) > 4000:
        chunks = [response[i:i+4000] for i in range(0, len(response), 4000)]
        for chunk in chunks:
            await update.message.reply_text(chunk)
    else:
        await update.message.reply_text(response)

def main():
    """Start the bot"""
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("=" * 50)
        print("ERROR: Set your Telegram bot token!")
        print("=" * 50)
        print(f"\nOpen config.json and set telegram_bot_token.")
        print(f"File: {CONFIG_FILE}")
        return

    print("Starting bot...")
    print(f"Claude CLI: {CLAUDE_CMD}")
    print(f"Working directory: {WORKING_DIR}")
    print("\nCommands:")
    print("  /start   - Get your Telegram ID")
    print("  /reset   - Reset session (new conversation)")
    print("  /cd      - Change working directory")
    print("  /pwd     - Show current directory")
    print("  /getfile - Download a file")
    print("\nPress Ctrl+C to stop")
    print("-" * 50)

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("reset", reset_command))
    app.add_handler(CommandHandler("cd", cd_command))
    app.add_handler(CommandHandler("pwd", pwd_command))
    app.add_handler(CommandHandler("getfile", getfile_command))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()

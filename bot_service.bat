@echo off
title Claude Telegram Bot Service
cd /d "%~dp0"

:loop
echo [%date% %time%] Starting bot...
python telegram_claude_bot.py

echo [%date% %time%] Bot stopped! Restarting in 5 seconds...
timeout /t 5 /nobreak >nul
goto loop

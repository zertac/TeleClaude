@echo off
echo Stopping Claude Telegram Bot...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *telegram_claude_bot*" 2>nul
taskkill /F /FI "WINDOWTITLE eq Claude Telegram Bot Service" 2>nul
for /f "tokens=2" %%a in ('tasklist /v ^| findstr /i "telegram_claude_bot"') do taskkill /F /PID %%a 2>nul
echo Bot stopped.
pause

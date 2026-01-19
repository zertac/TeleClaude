@echo off
echo Removing Claude Bot from Windows startup...

del "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\claude_bot.vbs" 2>nul

echo.
echo Done! Bot will no longer start with Windows.
echo.
pause

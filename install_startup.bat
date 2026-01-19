@echo off
echo Adding Claude Bot to Windows startup...

set "STARTUP=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "SCRIPT_DIR=%~dp0"

:: Create VBS file (runs batch file in hidden window)
(
echo Set WshShell = CreateObject^("WScript.Shell"^)
echo WshShell.Run chr^(34^) ^& "%SCRIPT_DIR%bot_service.bat" ^& chr^(34^), 0
echo Set WshShell = Nothing
) > "%STARTUP%\claude_bot.vbs"

echo.
echo Done!
echo Bot will now start automatically with Windows.
echo.
echo VBS file: %STARTUP%\claude_bot.vbs
echo.
pause

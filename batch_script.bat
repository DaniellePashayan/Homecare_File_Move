@Echo Starting Home Care File Move

SETLOCAL
set FILE_PATH=%~dp0
set SCRIPT_PATH=%FILE_PATH%main.py
python -u "%SCRIPT_PATH%"
ENDLOCAL

@Echo Process Completed

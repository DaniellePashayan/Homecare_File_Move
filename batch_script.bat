@Echo Starting File Move

setlocal
set "FILE_PATH=%~dp0.."
set "SCRIPT_PATH=%FILE_PATH%\main.py"
python -u "%SCRIPT_PATH%"
endlocal

python -u "%SCRIPT_PATH%"
@Echo Process Completed

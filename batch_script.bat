@echo off
echo Starting Home Care File Move

SETLOCAL
set FILE_PATH="C:\Users\pa_dpashayan\Desktop\PyProjects\Homecare_File_Move"
cd %FILE_PATH%
set SCRIPT_PATH=%FILE_PATH%\main.py
set VENV_PATH=%FILE_PATH\%.venv
set LOG_FILE=%FILE_PATH%\logs\error.txt

call "%VENV_PATH%\Scripts\activate.bat"
python -u "%SCRIPT_PATH%" >"%LOG_FILE%" 2>&1

IF ERRORLEVEL 1 (
    echo Python script encountered an error. The error message is: %ERRORLEVEL% %ERRORMESSAGE%
)
ENDLOCAL

Echo Process Completed
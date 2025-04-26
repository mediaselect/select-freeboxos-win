@echo off
setlocal

set VENV_PATH=C:\Venvs\select_freeboxos
set PYTHON_EXEC=%VENV_PATH%\Scripts\python.exe
set PYTHON_SCRIPT=C:\Apps\select_freeboxos\cron_select.py
set LOGFILE=%LOCALAPPDATA%\select_freeboxos\logs\cron_log.txt

if not exist "%LOCALAPPDATA%\select_freeboxos\logs" (
    mkdir "%LOCALAPPDATA%\select_freeboxos\logs"
)

echo =========================== >> %LOGFILE%
echo START TIME: %date% %time% >> %LOGFILE%
echo USERNAME: %USERNAME% >> %LOGFILE%
echo --------------------------- >> %LOGFILE%

timeout /t 20 /nobreak

"%PYTHON_EXEC%" "%PYTHON_SCRIPT%" >> %LOGFILE% 2>&1

echo --------------------------- >> %LOGFILE%
echo END TIME: %date% %time% >> %LOGFILE%
echo =========================== >> %LOGFILE%
echo. >> %LOGFILE%

endlocal

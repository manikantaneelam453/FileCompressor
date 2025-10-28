@echo off
setlocal EnableDelayedExpansion

title FileCompressor Launcher
mode con: cols=80 lines=25
color 0A

echo.
echo ╔══════════════════════════════════════════════╗
echo ║             FILECOMPRESSOR LAUNCHER          ║
echo ║          One-Click Application Start         ║
echo ║           developed by :life_learner         ║
echo ╚══════════════════════════════════════════════╝
echo.

:: Check Python
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Opening download page...
    start https://www.python.org/downloads/
    timeout /t 5
    exit /b 1
)
echo ✅ Python found

:: Install dependencies
echo [2/5] Installing dependencies...
cd backend
python -m pip install -r requirements.txt >nul 2>&1
if errorlevel 1 (
    echo ❌ Dependencies installation failed
    pause
    exit /b 1
)
echo ✅ Dependencies installed

:: Create folders
echo [3/5] Setting up folders...
mkdir uploads >nul 2>&1
mkdir compressed >nul 2>&1
echo ✅ Folders created

:: Start servers
echo [4/5] Starting servers...
start "FileCompressor Backend" /MIN cmd /c "python app.py"
timeout /t 3 >nul

cd ..\frontend
start "FileCompressor Frontend" /MIN cmd /c "python -m http.server 8000"
timeout /t 3 >nul

echo [5/5] Opening application...
start "" "http://localhost:8000"
echo ✅ Application opened in browser

echo.
echo ╔══════════════════════════════════════════════╗
echo ║                 APPLICATION READY            ║
echo ╠══════════════════════════════════════════════╣
echo ║  🌐 Web Interface: http://localhost:8000     ║
echo ║  ⚙️  Backend API:   http://localhost:5000     ║
echo ║                                              ║
echo ║  To stop the application:                    ║
echo ║  1. Press Win+R, type 'taskmgr'              ║
echo ║  2. End 'python.exe' processes               ║
echo ║  OR run the StopFileCompressor.bat file      ║
echo ╚══════════════════════════════════════════════╝
echo.
echo Press any key to create a desktop shortcut...
pause >nul

:: Create desktop shortcut
call :CreateShortcut
echo.
echo Press any key to exit...
pause >nul
exit /b

:CreateShortcut
echo Creating desktop shortcut...
set SCRIPT="%TEMP%\%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%.vbs"
echo Set oWS = WScript.CreateObject("WScript.Shell") > %SCRIPT%
echo sLinkFile = "%USERPROFILE%\Desktop\FileCompressor.lnk" >> %SCRIPT%
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SCRIPT%
echo oLink.TargetPath = "%~dp0FileCompressorLauncher.bat" >> %SCRIPT%
echo oLink.WorkingDirectory = "%~dp0" >> %SCRIPT%
echo oLink.Description = "FileCompressor Application" >> %SCRIPT%
echo oLink.Save >> %SCRIPT%
cscript /nologo %SCRIPT%
del %SCRIPT%
echo ✅ Desktop shortcut created!
goto :eof
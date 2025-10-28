@echo off
title FileCompressor - One Click App
chcp 65001 >nul
echo.
echo |==========================================|
echo |       FileCompressor Application         |
echo |           developed by : life_learner... |
echo |==========================================|
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo Please install Python from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

:: Install dependencies if needed
echo Checking dependencies...
cd backend
python -m pip install -r requirements.txt >nul 2>&1

:: Create necessary folders
mkdir uploads >nul 2>&1
mkdir compressed >nul 2>&1

echo Starting servers...
echo.

:: Start backend server (hidden)
start /B python app.py

:: Wait for backend to start
timeout /t 3 /nobreak >nul

:: Start frontend server (hidden)  
cd ..\frontend
start /B python -m http.server 8000

:: Wait for frontend to start
timeout /t 3 /nobreak >nul

echo ========================================
echo    FileCompressor is now running!
echo ========================================
echo.
echo Backend Server: http://localhost:5000
echo Web Interface: http://localhost:8000
echo.
echo Opening application...
echo.

:: Open browser
start http://localhost:8000

echo Press any key to stop the application and close...
pause >nul

:: Kill Python processes
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im pythonw.exe >nul 2>&1

echo Application stopped.
timeout /t 2 >nul
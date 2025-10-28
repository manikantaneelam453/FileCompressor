@echo off
title Stopping FileCompressor
echo Stopping FileCompressor application...
echo.
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im pythonw.exe >nul 2>&1
echo ✅ All FileCompressor processes stopped
echo.
echo Press any key to close...
pause >nul
@echo off
title MySQL Post Migration Tool
echo ===================================================
echo Starting migration from posts.json to MySQL...
echo ===================================================
echo.

cd /d "%~dp0"

echo [1/2] Installing required database libraries...
.\venv\Scripts\pip install -r requirements.txt

echo.
echo [2/2] Running migration script...
.\venv\Scripts\python migrate_data.py

echo.
echo ===================================================
echo Migration Complete! You can close this window now.
echo ===================================================
pause

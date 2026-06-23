@echo off
title FastAPI Backend Server
echo ===================================================
echo Starting FastAPI Backend with MySQL...
echo ===================================================
echo.

cd /d "%~dp0"

.\venv\Scripts\python main.py

pause

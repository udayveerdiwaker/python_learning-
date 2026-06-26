@echo off
title Python Practice Lab - Module 01: Basics
cls
echo =======================================================
echo     Python Practice Lab - Module 01: Python Basics
echo =======================================================
echo.

:: Detect virtual environment relative to the module folder
set VENV_PATH=..\..\venv\Scripts\python.exe
if not exist "%VENV_PATH%" (
    set VENV_PATH=python
)

echo Using Python interpreter: %VENV_PATH%
echo.

echo -------------------------------------------------------
echo 1. Running basics.py (Tutorial and Examples)
echo -------------------------------------------------------
"%VENV_PATH%" basics.py
if %ERRORLEVEL% neq 0 (
    echo.
    echo [WARNING] basics.py failed to run. Make sure Python is installed.
)
echo.
pause

cls
echo =======================================================
echo 2. Running exercises.py (Automated Tests)
echo =======================================================
echo.
:: Set UTF-8 encoding environment variable for python output
set PYTHONUTF8=1
"%VENV_PATH%" exercises.py
if %ERRORLEVEL% neq 0 (
    echo.
    echo [WARNING] exercises.py failed to run or some assertions failed.
)
echo.
pause

cls
echo =======================================================
echo 3. Would you like to run the interactive RPG Simulator?
echo =======================================================
echo.
set /p choice="Run challenge.py? (Y/N): "
if /i "%choice%"=="Y" (
    cls
    "%VENV_PATH%" challenge.py
)

echo.
echo =======================================================
echo Practice session finished!
echo =======================================================
pause

@echo off
chcp 65001 >nul 2>&1

:: Check if already running as admin
if "%1"=="ELEV" goto :admin

:: Check for administrator privileges
net session >nul 2>&1
if %errorlevel% == 0 goto :admin

:: Request administrator privileges
echo Requesting administrator privileges...
powershell -Command "Start-Process '%~f0' -ArgumentList 'ELEV' -Verb RunAs"
exit /b

:admin
echo Administrator privileges confirmed

cd /d "%~dp0"
echo Starting Network Configuration Tool...
python main.py
if %errorlevel% neq 0 (
    echo.
    echo Program execution failed, please check:
    echo 1. Python is installed
    echo 2. Dependencies are installed ^(pip install -r requirements.txt^)
    echo 3. PyQt5 is properly installed
    echo.
    pause
)
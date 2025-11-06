@echo off
title Tennis Ball Tracker GUI
echo 🎾 Starting Tennis Ball Tracker GUI...
echo.

cd /d "%~dp0"
"%~dp0venv\Scripts\python.exe" run_gui.py

pause
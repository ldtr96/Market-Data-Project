@echo off
REM Change to the directory where this batch file is located
cd /d "%~dp0"
REM The below will be executed by Windows Task Scheduler.
"%~dp0\.venv\Scripts\python.exe" main.py --ticker AAPL
"%~dp0\.venv\Scripts\python.exe" main.py --ticker MSFT
"%~dp0\.venv\Scripts\python.exe" main.py --ticker NVDA
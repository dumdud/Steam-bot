@echo off
call "%~dp0.venv\scripts\activate.bat"
start pythonw "%~dp0main.py"
exit 0
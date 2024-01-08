@echo on
call "%~dp0.venv\scripts\activate.bat"
start python "%~dp0main.py"
pause
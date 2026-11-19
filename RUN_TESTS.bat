@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Run START_ASSIGNMENT.bat once first to create the environment.
  pause
  exit /b 1
)
call .venv\Scripts\activate.bat
python -m pip install -e ".[dev]"
ruff check .
mypy src
pytest --cov=regression_lab --cov-report=term-missing --cov-fail-under=80
pause

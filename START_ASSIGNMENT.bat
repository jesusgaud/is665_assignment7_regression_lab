@echo off
setlocal
cd /d "%~dp0"
echo ============================================================
echo IS 665 Assignment 7 - Regression Analysis Lab
echo ============================================================

where py >nul 2>nul
if errorlevel 1 (
  echo ERROR: Python launcher "py" was not found.
  echo Install Python 3.11-3.15 and try again.
  pause
  exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
  echo Creating virtual environment...
  py -3.15 -m venv .venv 2>nul
  if errorlevel 1 py -3 -m venv .venv
  if errorlevel 1 (
    echo ERROR: Could not create the virtual environment.
    pause
    exit /b 1
  )
)

call .venv\Scripts\activate.bat
python -m pip install --upgrade pip setuptools wheel
if errorlevel 1 goto :fail
python -m pip install -e .
if errorlevel 1 goto :fail
streamlit run app.py
goto :eof

:fail
echo.
echo Installation failed. Review the messages above.
pause
exit /b 1

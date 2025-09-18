@echo off
REM PDF Compressor Virtual Environment Activation Script for Windows
REM Run this script to activate the virtual environment

set VENV_DIR=venv_pdf

if not exist "%VENV_DIR%" (
    echo ❌ Virtual environment not found. Please run setup_pdf_compressor.bat first
    pause
    exit /b 1
)

echo 🔄 Activating PDF compressor virtual environment...
call %VENV_DIR%\Scripts\activate.bat

echo ✅ Virtual environment activated!
echo 📄 You can now use the PDF compressor:
echo    python pdf_compressor.py your_file.pdf
echo.
echo To deactivate when done, type: deactivate

REM Keep the command prompt open
cmd /k

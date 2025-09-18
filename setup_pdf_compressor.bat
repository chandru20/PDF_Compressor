@echo off
REM PDF Compressor Setup Script for Windows
REM This script installs the required dependencies for the PDF compressor

echo 🔧 Setting up PDF Compressor dependencies...

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Error: Python is not installed or not in PATH. Please install Python 3.6+ first.
    pause
    exit /b 1
)

echo ✅ Python found

REM Check if pip is available
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Error: pip is not installed or not in PATH. Please install pip first.
    pause
    exit /b 1
)

echo ✅ pip found

REM Create virtual environment if it doesn't exist
if not exist "venv_pdf" (
    echo 🔨 Creating virtual environment...
    python -m venv venv_pdf
    if %errorlevel% neq 0 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment already exists
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv_pdf\Scripts\activate.bat

REM Install Python dependencies
echo 📦 Installing Python dependencies...
pip3 install -r requirements_pdf.txt

if %errorlevel% equ 0 (
    echo ✅ Python dependencies installed successfully
) else (
    echo ❌ Failed to install Python dependencies
    pause
    exit /b 1
)

REM Check for Ghostscript
gs --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Ghostscript found - advanced compression available
) else (
    echo ⚠️  Ghostscript not found - install for better compression:
    echo    Windows: Download from https://www.ghostscript.com/download/gsdnld.html
    echo    Or use chocolatey: choco install ghostscript
    echo    Or use winget: winget install AGPL.Ghostscript
)

REM Make the script executable (not needed on Windows, but for consistency)
echo.

echo 🎉 Setup complete!
echo.
echo 📝 To use the PDF compressor:
echo 1. Activate the virtual environment:
echo    venv_pdf\Scripts\activate.bat
echo    # OR use the helper script: activate_pdf_env.bat
echo.
echo 2. Run the compressor:
echo    python pdf_compressor.py document.pdf
echo    python pdf_compressor.py document.pdf -o compressed.pdf -q high
echo    python pdf_compressor.py *.pdf -d compressed\ -q medium
echo.
echo 3. When done, deactivate:
echo    deactivate
echo.
echo For help: python pdf_compressor.py --help

pause

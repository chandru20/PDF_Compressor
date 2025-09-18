#!/bin/bash

# PDF Compressor Setup Script
# This script installs the required dependencies for the PDF compressor

echo "🔧 Setting up PDF Compressor dependencies..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "✅ Python 3 found"

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ Error: pip3 is not installed. Please install pip first."
    exit 1
fi

echo "✅ pip3 found"

# Create virtual environment if it doesn't exist
VENV_DIR="venv_pdf"
if [ ! -d "$VENV_DIR" ]; then
    echo "🔨 Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements_pdf.txt

if [ $? -eq 0 ]; then
    echo "✅ Python dependencies installed successfully"
else
    echo "❌ Failed to install Python dependencies"
    exit 1
fi

# Check for Ghostscript (optional but recommended)
if command -v gs &> /dev/null; then
    echo "✅ Ghostscript found - advanced compression available"
else
    echo "⚠️  Ghostscript not found - install for better compression:"
    echo "   macOS: brew install ghostscript"
    echo "   Ubuntu/Debian: sudo apt-get install ghostscript"
    echo "   CentOS/RHEL: sudo yum install ghostscript"
fi

# Make the script executable
chmod +x pdf_compressor.py

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📝 To use the PDF compressor:"
echo "1. Activate the virtual environment:"
echo "   source venv_pdf/bin/activate"
echo "   # OR use the helper script: source activate_pdf_env.sh"
echo ""
echo "2. Run the compressor:"
echo "   python pdf_compressor.py document.pdf"
echo "   python pdf_compressor.py document.pdf -o compressed.pdf -q high"
echo "   python pdf_compressor.py *.pdf -d compressed/ -q medium"
echo ""
echo "3. When done, deactivate:"
echo "   deactivate"
echo ""
echo "For help: python pdf_compressor.py --help"

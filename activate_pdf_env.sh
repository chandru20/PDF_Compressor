#!/bin/bash

# PDF Compressor Virtual Environment Activation Script
# Source this script to activate the virtual environment

VENV_DIR="venv_pdf"

if [ ! -d "$VENV_DIR" ]; then
    echo "❌ Virtual environment not found. Please run ./setup_pdf_compressor.sh first"
    return 1
fi

echo "🔄 Activating PDF compressor virtual environment..."
source "$VENV_DIR/bin/activate"

echo "✅ Virtual environment activated!"
echo "📄 You can now use the PDF compressor:"
echo "   python pdf_compressor.py your_file.pdf"
echo ""
echo "To deactivate when done, type: deactivate"

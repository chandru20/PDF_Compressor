#!/bin/bash

# PDF Compressor Demo Script
# This script demonstrates various ways to use the PDF compressor

echo "📄 PDF Compressor Demo"
echo "====================="
echo ""

# Check if the script exists
if [ ! -f "pdf_compressor.py" ]; then
    echo "❌ pdf_compressor.py not found in current directory"
    echo "   Please run this script from the directory containing pdf_compressor.py"
    exit 1
fi

echo "This demo shows how to use the PDF compressor with different options."
echo "Note: You'll need actual PDF files to test with."
echo ""

echo "🔧 1. First, set up the dependencies:"
echo "   ./setup_pdf_compressor.sh"
echo ""

echo "� 2. Activate the virtual environment:"
echo "   source venv_pdf/bin/activate"
echo "   # OR: source activate_pdf_env.sh"
echo ""

echo "�📝 3. Basic usage examples:"
echo ""

echo "   # Compress a single PDF with default settings (medium quality)"
echo "   python pdf_compressor.py document.pdf"
echo ""

echo "   # Compress with high quality and specify output file"
echo "   python pdf_compressor.py document.pdf -o compressed_document.pdf -q high"
echo ""

echo "   # Compress with maximum compression for smallest file size"
echo "   python pdf_compressor.py large_file.pdf -q maximum"
echo ""

echo "📁 4. Batch processing examples:"
echo ""

echo "   # Compress all PDFs in current directory to a 'compressed' folder"
echo "   python pdf_compressor.py *.pdf -d compressed/"
echo ""

echo "   # Compress specific files with high compression"
echo "   python pdf_compressor.py file1.pdf file2.pdf file3.pdf -q high -d output/"
echo ""

echo "   # Compress all PDFs in Documents folder"
echo "   python pdf_compressor.py ~/Documents/*.pdf -d ~/compressed_pdfs/"
echo ""

echo "🔍 5. Advanced options:"
echo ""

echo "   # Verbose output to see detailed information"
echo "   python pdf_compressor.py document.pdf -q high -v"
echo ""

echo "   # Get help and see all options"
echo "   python pdf_compressor.py --help"
echo ""

echo "📊 6. Compression levels:"
echo "   • low     - Low compression, high quality (best for images)"
echo "   • medium  - Balanced compression and quality (default)"
echo "   • high    - High compression, good quality (recommended)"
echo "   • maximum - Maximum compression, lower quality (smallest files)"
echo ""

echo "🧪 7. Test the installation:"
echo "   python test_pdf_compressor.py"
echo ""

echo "💡 Tips:"
echo "   • Install Ghostscript for better compression results"
echo "   • Use 'medium' or 'high' quality for most documents"
echo "   • Use batch processing for multiple files"
echo "   • Check file sizes before and after compression"
echo ""

echo "🚀 Ready to compress your PDFs!"

# If user wants to run a test
read -p "Do you want to test the compressor setup now? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Activating virtual environment and running test..."
    source venv_pdf/bin/activate
    python test_pdf_compressor.py
    deactivate
fi

# PDF Compressor

A comprehensive, cross-platform Python utility for compressing PDF files with multiple quality levels and batch processing capabilities. Works on macOS, Linux, and Windows.

---

## 🚀 Quick Start

### 1. Setup (First Time Only)

#### On macOS/Linux:
```bash
./setup_pdf_compressor.sh
```
#### On Windows:
```bat
setup_pdf_compressor.bat
```

### 2. Activate the Virtual Environment

#### On macOS/Linux:
```bash
source venv_pdf/bin/activate
```
#### On Windows:
```bat
venv_pdf\Scripts\activate.bat
```
Or use the helper script:
```bash
source activate_pdf_env.sh      # macOS/Linux
activate_pdf_env.bat           # Windows
```

### 3. Compress PDFs
```bash
python pdf_compressor.py document.pdf                         # Basic compression
python pdf_compressor.py document.pdf -q high                 # High compression
python pdf_compressor.py document.pdf --target-size-mb 1.0    # Target under 1 MB
python pdf_compressor.py *.pdf -d compressed/                 # Batch processing
```

### 4. When Done
```bash
deactivate
```

---

## Features
- **Smart Target Sizing**: Automatically finds best quality for your size target
- **Multiple Compression Levels**: low, medium, high, maximum
- **Batch Processing**: Compress multiple PDFs at once
- **Balanced Quality**: Uses advanced Ghostscript settings for optimal quality/size ratio
- **Progress Tracking**: File sizes and compression ratios
- **Cross-platform**: macOS, Linux, Windows

---

## Command Line Options
| Option | Description | Example |
|--------|-------------|---------|
| `-o, --output` | Output file path (single file only) | `-o compressed.pdf` |
| `-d, --output-dir` | Output directory for compressed files | `-d compressed/` |
| `-q, --quality` | Compression quality (low/medium/high/maximum) | `-q high` |
| `--target-size-mb` | Try to compress under this size (MB); iteratively picks a suitable Ghostscript preset | `--target-size-mb 1.0` |
| `-v, --verbose` | Enable verbose output | `-v` |
| `--help` | Show help message | `--help` |

---

## Compression Levels
| Level | Description | Use Case |
|-------|-------------|----------|
| `low` | Low compression, high quality | Documents with important image quality |
| `medium` | Balanced compression and quality (default) | General purpose compression |
| `high` | High compression, good quality | Reducing file size while maintaining readability |
| `maximum` | Maximum compression, lower quality | Minimize file size for storage/transmission |

---

## Examples
### Target Size Compression (Recommended)
```bash
python pdf_compressor.py document.pdf --target-size-mb 1.0    # Under 1 MB with best quality
python pdf_compressor.py document.pdf --target-size-mb 0.5    # Under 500 KB 
python pdf_compressor.py document.pdf --target-size-mb 2.0    # Under 2 MB (preserves quality)
```

### Traditional Quality Levels
```bash
python pdf_compressor.py document.pdf                         # Default (medium)
python pdf_compressor.py document.pdf -q high                 # High compression
python pdf_compressor.py document.pdf -q maximum              # Maximum compression
```
### Batch Processing
```bash
python pdf_compressor.py *.pdf -d compressed/
python pdf_compressor.py file1.pdf file2.pdf file3.pdf -q high -d output/
python pdf_compressor.py documents/*.pdf -d compressed_docs/ -q medium
```
### Advanced Usage
```bash
python pdf_compressor.py *.pdf -d compressed/ -q high -v
python pdf_compressor.py ~/Documents/*.pdf ~/Downloads/*.pdf -d ~/compressed_pdfs/
```

---

## Output Information
- Original file size
- Compressed file size
- Compression ratio (percentage reduction)
- Processing status for each file
- Summary of batch operations

Example output:
```
2024-08-14 10:30:15 - INFO - Compressing: document.pdf (2.5 MB)
2024-08-14 10:30:16 - INFO - Compressed: document_compressed.pdf (1.8 MB) - 28.0% reduction
```

---

## Dependencies
- **Python 3.6+**
- **PyPDF2** or **pypdf**: Core PDF processing library
- **Pillow (PIL)**: For advanced image processing
- **Ghostscript**: For superior compression results (highly recommended)

---

## Troubleshooting & Performance Tips
- **"No PDF processing libraries available"**: Install PyPDF2 with `pip install PyPDF2`
- **Poor compression results**: Install Ghostscript for better compression algorithms
- **Permission errors**: Ensure you have write permissions to the output directory
- **Large files timing out**: Use verbose mode (`-v`) to monitor progress
- **Use Ghostscript**: Install for significantly better compression
- **Choose appropriate quality**: Use `medium` for general use, `high` for important documents
- **Batch processing**: Process multiple files at once for efficiency
- **Output directory**: Use `-d` option for organized output when processing many files

---

## Platform Support
- **macOS**: Fully supported
- **Linux**: Fully supported
- **Windows**: Fully supported (use `python` instead of `python3`)

---

## File Structure
```
PDF_Compressor/
├── pdf_compressor.py              # Main compression script
├── venv_pdf/                      # Virtual environment (auto-created)
├── setup_pdf_compressor.sh        # Setup script (macOS/Linux)
├── setup_pdf_compressor.bat       # Setup script (Windows)
├── activate_pdf_env.sh            # Environment activation helper (macOS/Linux)
├── activate_pdf_env.bat           # Environment activation helper (Windows)
├── test_pdf_compressor.py         # Test script
├── demo_pdf_compressor.sh         # Demo and examples (macOS/Linux)
├── demo_pdf_compressor.bat        # Demo and examples (Windows)
├── requirements_pdf.txt           # Python dependencies
└── README.md                      # Documentation (this file)
```

---

## License
This script is provided as-is for educational and practical use. Feel free to modify and distribute.

---

For more help, run:
```bash
python pdf_compressor.py --help
python test_pdf_compressor.py
```

Happy compressing! 📄✨

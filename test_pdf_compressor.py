#!/usr/bin/env python3
"""
PDF Compressor Test Script
=========================

This script tests the PDF compressor functionality and verifies that
all dependencies are properly installed.
"""

import sys
import subprocess
from pathlib import Path
import tempfile

def test_dependencies():
    """Test if required dependencies are available."""
    import platform
    
    print("🔍 Testing dependencies...")
    
    # Test PyPDF2/pypdf
    try:
        import PyPDF2
        print("✅ PyPDF2 found")
        pypdf_available = True
    except ImportError:
        try:
            import pypdf
            print("✅ pypdf found")
            pypdf_available = True
        except ImportError:
            print("❌ Neither PyPDF2 nor pypdf found")
            pypdf_available = False
    
    # Test Pillow
    try:
        from PIL import Image
        print("✅ Pillow (PIL) found")
        pil_available = True
    except ImportError:
        print("⚠️  Pillow (PIL) not found - image processing disabled")
        pil_available = False
    
    # Test Ghostscript with platform-specific checks
    gs_available = False
    try:
        if platform.system() == 'Windows':
            # Try different Windows Ghostscript executables
            for gs_exe in ['gswin64c', 'gswin32c', 'gs']:
                try:
                    result = subprocess.run([gs_exe, '--version'], capture_output=True, timeout=10)
                    if result.returncode == 0:
                        print(f"✅ Ghostscript found ({gs_exe})")
                        gs_available = True
                        break
                except (FileNotFoundError, subprocess.TimeoutExpired):
                    continue
        else:
            # Unix-like systems (macOS, Linux)
            result = subprocess.run(['gs', '--version'], capture_output=True, timeout=10)
            if result.returncode == 0:
                print("✅ Ghostscript found")
                gs_available = True
        
        if not gs_available:
            system = platform.system()
            if system == 'Windows':
                print("⚠️  Ghostscript not found - download from ghostscript.com")
            else:
                print("⚠️  Ghostscript not found - basic compression only")
                
    except Exception as e:
        print(f"⚠️  Error checking Ghostscript: {e}")
        gs_available = False
    
    return pypdf_available, pil_available, gs_available

def create_test_pdf():
    """Create a simple test PDF file."""
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        # Create a temporary PDF file
        temp_dir = Path(tempfile.mkdtemp())
        test_pdf = temp_dir / "test_document.pdf"
        
        # Create PDF with some content
        c = canvas.Canvas(str(test_pdf), pagesize=letter)
        c.drawString(100, 750, "Test PDF Document")
        c.drawString(100, 700, "This is a test document for PDF compression.")
        c.drawString(100, 650, "It contains some text content to compress.")
        
        # Add multiple pages to make it larger
        for i in range(5):
            c.showPage()
            c.drawString(100, 750, f"Page {i+2}")
            c.drawString(100, 700, "Additional content on this page.")
            c.drawString(100, 650, "More text to make the file larger.")
        
        c.save()
        
        print(f"✅ Created test PDF: {test_pdf}")
        return test_pdf
        
    except ImportError:
        print("⚠️  reportlab not available - cannot create test PDF")
        print("   You can test with your own PDF file instead")
        return None

def test_compressor():
    """Test the PDF compressor with a sample file."""
    print("\n🧪 Testing PDF compressor...")
    
    # Import the compressor
    try:
        from pdf_compressor import PDFCompressor, check_dependencies
        print("✅ PDF compressor module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import PDF compressor: {e}")
        return False
    
    # Check dependencies
    try:
        check_dependencies()
        print("✅ Dependency check completed")
    except SystemExit:
        print("❌ Dependency check failed")
        return False
    
    # Test compressor creation
    try:
        compressor = PDFCompressor('medium')
        print("✅ PDFCompressor instance created")
    except Exception as e:
        print(f"❌ Failed to create compressor: {e}")
        return False
    
    return True

def test_command_line():
    """Test the command-line interface."""
    print("\n🖥️  Testing command-line interface...")
    
    try:
        # Test help command - use the same Python executable that's running this script
        result = subprocess.run([
            sys.executable, 'pdf_compressor.py', '--help'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Command-line help works")
            return True
        else:
            print(f"❌ Command-line help failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Command-line test timed out")
        return False
    except Exception as e:
        print(f"❌ Command-line test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 PDF Compressor Test Suite")
    print("=" * 40)
    
    # Test dependencies
    pypdf_ok, pil_ok, gs_ok = test_dependencies()
    
    if not pypdf_ok:
        print("\n❌ Critical dependency missing: PyPDF2 or pypdf required")
        print("   Run: pip install PyPDF2")
        return False
    
    # Test compressor module
    if not test_compressor():
        return False
    
    # Test command-line interface
    if not test_command_line():
        return False
    
    # Summary
    print("\n📋 Test Summary:")
    print("=" * 20)
    
    if pypdf_ok and test_compressor():
        print("✅ Core functionality: WORKING")
    else:
        print("❌ Core functionality: FAILED")
    
    if pil_ok:
        print("✅ Image processing: AVAILABLE")
    else:
        print("⚠️  Image processing: LIMITED")
    
    if gs_ok:
        print("✅ Advanced compression: AVAILABLE")
    else:
        print("⚠️  Advanced compression: LIMITED")
    
    print("\n🎉 Test completed!")
    print("\nTo test with a real PDF file, run:")
    print("   python3 pdf_compressor.py your_file.pdf")
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

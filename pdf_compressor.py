#!/usr/bin/env python3
"""
PDF Compression Script
=====================

A comprehensive tool for compressing PDF files with various compression levels
and options. Supports both individual files and batch processing.

Features:
- Multiple compression levels (low, medium, high, maximum)
- Batch processing for multiple files
- Custom output directory support
- Progress tracking and file size reporting
- Quality preservation options
- Command-line interface

Requirements:
- PyPDF2 or pypdf (for basic compression)
- Pillow (PIL) for image processing
- Optional: Ghostscript for advanced compression

Usage:
    python pdf_compressor.py input.pdf
    python pdf_compressor.py input.pdf -o output.pdf -q medium
    python pdf_compressor.py *.pdf -d output_folder -q high
"""

import os
import sys
import argparse
import logging
from pathlib import Path
from typing import List, Optional, Tuple
import tempfile
import shutil

try:
    import PyPDF2
    from PyPDF2 import PdfReader, PdfWriter
    PYPDF_AVAILABLE = True
except ImportError:
    try:
        import pypdf
        from pypdf import PdfReader, PdfWriter
        PYPDF_AVAILABLE = True
    except ImportError:
        PYPDF_AVAILABLE = False

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class PDFCompressor:
    """
    PDF Compression utility class with multiple compression strategies.
    """
    
    COMPRESSION_LEVELS = {
        'low': {
            'description': 'Low compression, high quality',
            'image_quality': 85,
            'image_dpi': 150,
            'remove_duplicates': False
        },
        'medium': {
            'description': 'Balanced compression and quality',
            'image_quality': 75,
            'image_dpi': 120,
            'remove_duplicates': True
        },
        'high': {
            'description': 'High compression, good quality',
            'image_quality': 60,
            'image_dpi': 100,
            'remove_duplicates': True
        },
        'maximum': {
            'description': 'Maximum compression, lower quality',
            'image_quality': 45,
            'image_dpi': 72,
            'remove_duplicates': True
        }
    }
    
    def __init__(self, compression_level: str = 'medium', target_size_bytes: Optional[int] = None):
        """
        Initialize the PDF compressor.
        
        Args:
            compression_level: Compression level ('low', 'medium', 'high', 'maximum')
        """
        if compression_level not in self.COMPRESSION_LEVELS:
            raise ValueError(f"Invalid compression level. Choose from: {list(self.COMPRESSION_LEVELS.keys())}")
        
        self.compression_level = compression_level
        self.settings = self.COMPRESSION_LEVELS[compression_level]
        self.target_size_bytes = target_size_bytes
        
        # Check dependencies
        if not PYPDF_AVAILABLE:
            logger.warning("PyPDF2/pypdf not available. Limited compression features.")
        if not PIL_AVAILABLE:
            logger.warning("Pillow not available. Image compression disabled.")
    
    def get_file_size(self, file_path: Path) -> int:
        """Get file size in bytes."""
        return file_path.stat().st_size
    
    def format_size(self, size_bytes: int) -> str:
        """Format file size in human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"
    
    def compress_with_pypdf(self, input_path: Path, output_path: Path) -> bool:
        """
        Compress PDF using PyPDF2/pypdf library.
        
        Args:
            input_path: Path to input PDF
            output_path: Path to output PDF
            
        Returns:
            bool: Success status
        """
        try:
            with open(input_path, 'rb') as input_file:
                pdf_reader = PdfReader(input_file)
                pdf_writer = PdfWriter()
                
                # Copy pages with compression
                for page_num, page in enumerate(pdf_reader.pages):
                    # Remove duplicate objects if enabled
                    if self.settings['remove_duplicates']:
                        page.compress_content_streams()
                    
                    pdf_writer.add_page(page)
                
                # Write compressed PDF
                with open(output_path, 'wb') as output_file:
                    pdf_writer.write(output_file)
                
                return True
                
        except Exception as e:
            logger.error(f"PyPDF compression failed: {e}")
            return False
    
    def compress_with_ghostscript(self, input_path: Path, output_path: Path, override_quality: Optional[str] = None) -> bool:
        """
        Compress PDF using Ghostscript (if available).
        
        Args:
            input_path: Path to input PDF
            output_path: Path to output PDF
            
        Returns:
            bool: Success status
        """
        try:
            import subprocess
            import platform
            
            # Map compression levels to Ghostscript settings
            gs_settings = {
                'low': '/ebook',
                'medium': '/printer',
                'high': '/prepress',
                'maximum': '/screen'
            }
            
            if override_quality is not None:
                gs_quality = override_quality
            else:
                gs_quality = gs_settings.get(self.compression_level, '/printer')
            
            # Determine Ghostscript executable name based on platform
            if platform.system() == 'Windows':
                gs_executable = 'gswin64c'  # Try 64-bit version first
                try:
                    # Test if gswin64c exists
                    subprocess.run([gs_executable, '--version'], capture_output=True, check=True)
                except (subprocess.CalledProcessError, FileNotFoundError):
                    gs_executable = 'gswin32c'  # Fallback to 32-bit
                    try:
                        subprocess.run([gs_executable, '--version'], capture_output=True, check=True)
                    except (subprocess.CalledProcessError, FileNotFoundError):
                        gs_executable = 'gs'  # Final fallback
            else:
                gs_executable = 'gs'
            
            # Ghostscript command with proper path handling
            cmd = [
                gs_executable,
                '-sDEVICE=pdfwrite',
                '-dCompatibilityLevel=1.4',
                f'-dPDFSETTINGS={gs_quality}',
                '-dNOPAUSE',
                '-dQUIET',
                '-dBATCH',
                f'-sOutputFile={output_path}',
                str(input_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                return True
            else:
                logger.error(f"Ghostscript error: {result.stderr}")
                return False
                
        except FileNotFoundError:
            logger.debug("Ghostscript not found")
            return False
        except Exception as e:
            logger.error(f"Ghostscript compression failed: {e}")
            return False
    
    def compress_with_ghostscript_advanced(self, input_path: Path, output_path: Path, 
                                         preset: str, image_dpi: int, jpeg_quality: int) -> bool:
        """
        Compress PDF using Ghostscript with fine-tuned image settings.
        
        Args:
            input_path: Path to input PDF
            output_path: Path to output PDF
            preset: Ghostscript preset (/prepress, /printer, /ebook, /screen)
            image_dpi: DPI for image downsampling
            jpeg_quality: JPEG quality (0-100)
            
        Returns:
            bool: Success status
        """
        try:
            import subprocess
            import platform
            
            # Determine Ghostscript executable name based on platform
            if platform.system() == 'Windows':
                gs_executable = 'gswin64c'
                try:
                    subprocess.run([gs_executable, '--version'], capture_output=True, check=True)
                except (subprocess.CalledProcessError, FileNotFoundError):
                    gs_executable = 'gswin32c'
                    try:
                        subprocess.run([gs_executable, '--version'], capture_output=True, check=True)
                    except (subprocess.CalledProcessError, FileNotFoundError):
                        gs_executable = 'gs'
            else:
                gs_executable = 'gs'
            
            # Advanced Ghostscript command with custom image settings
            cmd = [
                gs_executable,
                '-sDEVICE=pdfwrite',
                '-dCompatibilityLevel=1.4',
                f'-dPDFSETTINGS={preset}',
                '-dNOPAUSE',
                '-dQUIET',
                '-dBATCH',
                # Custom image settings for better quality control
                f'-dColorImageResolution={image_dpi}',
                f'-dGrayImageResolution={image_dpi}',
                f'-dMonoImageResolution={image_dpi * 2}',  # Higher for monochrome
                '-dColorImageDownsampleType=/Bicubic',
                '-dGrayImageDownsampleType=/Bicubic',
                f'-dJPEGQ={jpeg_quality}',
                '-dOptimize=true',
                '-dEmbedAllFonts=true',
                '-dSubsetFonts=true',
                f'-sOutputFile={output_path}',
                str(input_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                return True
            else:
                logger.debug(f"Advanced Ghostscript error: {result.stderr}")
                return False
                
        except FileNotFoundError:
            logger.debug("Ghostscript not found")
            return False
        except Exception as e:
            logger.debug(f"Advanced Ghostscript compression failed: {e}")
            return False
    
    def compress_file(self, input_path: Path, output_path: Optional[Path] = None) -> Tuple[bool, Path]:
        """
        Compress a single PDF file.
        
        Args:
            input_path: Path to input PDF file
            output_path: Optional path to output file
            
        Returns:
            Tuple[bool, Path]: (Success status, output file path)
        """
        if not input_path.exists():
            logger.error(f"Input file not found: {input_path}")
            return False, input_path
        
        if not input_path.suffix.lower() == '.pdf':
            logger.error(f"Not a PDF file: {input_path}")
            return False, input_path
        
        # Generate output path if not provided
        if output_path is None:
            output_path = input_path.parent / f"{input_path.stem}_compressed.pdf"
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        original_size = self.get_file_size(input_path)
        logger.info(f"Compressing: {input_path.name} ({self.format_size(original_size)})")
        
        # Try different compression methods
        success = False
        
        # If target size is requested, try balanced approach with multiple quality configurations
        if self.target_size_bytes is not None:
            # Quality configurations from best to most aggressive
            configs = [
                ('/prepress', 'high quality', 300, 90),
                ('/printer', 'good quality', 200, 80), 
                ('/printer', 'balanced', 150, 75),
                ('/ebook', 'compact', 150, 70),
                ('/screen', 'minimal', 100, 60),
            ]
            
            for preset, desc, dpi, jpeg_q in configs:
                temp_output = output_path.parent / f"temp_{output_path.name}"
                try:
                    if self.compress_with_ghostscript_advanced(input_path, temp_output, preset, dpi, jpeg_q):
                        if temp_output.exists():
                            size = self.get_file_size(temp_output)
                            logger.debug(f"Tried {desc}: {self.format_size(size)}")
                            
                            if size <= self.target_size_bytes:
                                # Found a configuration that meets target - use it
                                temp_output.rename(output_path)
                                success = True
                                logger.info(f"Achieved target size with {desc} compression")
                                break
                            else:
                                temp_output.unlink(missing_ok=True)
                except Exception as e:
                    logger.debug(f"Configuration {desc} failed: {e}")
                    temp_output.unlink(missing_ok=True)
            
            # If no config met the target, fall back to most aggressive
            if not success:
                logger.debug("No configuration met target size, using most aggressive")
                if self.compress_with_ghostscript(input_path, output_path, override_quality='/screen'):
                    success = True
        else:
            # Method 1: Try Ghostscript first (usually better compression)
            if self.compress_with_ghostscript(input_path, output_path):
                success = True
                logger.debug("Used Ghostscript compression")
            
            # Method 2: Fallback to PyPDF if Ghostscript fails
            elif PYPDF_AVAILABLE and self.compress_with_pypdf(input_path, output_path):
                success = True
                logger.debug("Used PyPDF compression")
        
        if success and output_path.exists():
            compressed_size = self.get_file_size(output_path)
            compression_ratio = (1 - compressed_size / original_size) * 100
            
            logger.info(f"Compressed: {output_path.name} ({self.format_size(compressed_size)}) "
                       f"- {compression_ratio:.1f}% reduction")
            
            return True, output_path
        else:
            logger.error(f"Failed to compress: {input_path.name}")
            return False, input_path
    
    def compress_batch(self, input_paths: List[Path], output_dir: Optional[Path] = None) -> List[Tuple[bool, Path, Path]]:
        """
        Compress multiple PDF files.
        
        Args:
            input_paths: List of input PDF file paths
            output_dir: Optional output directory
            
        Returns:
            List of (success, input_path, output_path) tuples
        """
        results = []
        total_files = len(input_paths)
        
        logger.info(f"Starting batch compression of {total_files} files...")
        logger.info(f"Compression level: {self.compression_level} - {self.settings['description']}")
        
        for i, input_path in enumerate(input_paths, 1):
            logger.info(f"Processing file {i}/{total_files}")
            
            # Determine output path
            if output_dir:
                output_dir.mkdir(parents=True, exist_ok=True)
                output_path = output_dir / f"{input_path.stem}_compressed.pdf"
            else:
                output_path = None
            
            success, final_output_path = self.compress_file(input_path, output_path)
            results.append((success, input_path, final_output_path))
        
        # Summary
        successful = sum(1 for success, _, _ in results if success)
        logger.info(f"Batch compression complete: {successful}/{total_files} files processed successfully")
        
        return results


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Compress PDF files with various quality settings',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s document.pdf                           # Compress with default settings
  %(prog)s document.pdf -o compressed.pdf         # Specify output file
  %(prog)s *.pdf -d compressed/                   # Batch compress to directory
  %(prog)s file.pdf -q high                       # Use high compression
  %(prog)s file.pdf --target-size-mb 1.0          # Target under 1 MB with balanced quality
        """
    )
    
    parser.add_argument(
        'input',
        nargs='+',
        help='Input PDF file(s) or pattern (e.g., *.pdf)'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=Path,
        help='Output file path (for single file only)'
    )
    
    parser.add_argument(
        '-d', '--output-dir',
        type=Path,
        help='Output directory for compressed files'
    )
    
    parser.add_argument(
        '-q', '--quality',
        choices=['low', 'medium', 'high', 'maximum'],
        default='medium',
        help='Compression quality level (default: medium)'
    )
    
    parser.add_argument(
        '--target-size-mb',
        type=float,
        help='Try to compress under this size in megabytes (iterates Ghostscript presets to find a good balance)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='PDF Compressor 1.0.0'
    )
    
    return parser.parse_args()


def expand_file_patterns(patterns: List[str]) -> List[Path]:
    """
    Expand file patterns and glob expressions to actual file paths.
    
    Args:
        patterns: List of file patterns or paths
        
    Returns:
        List of Path objects for existing PDF files
    """
    import glob
    
    files = []
    for pattern in patterns:
        if '*' in pattern or '?' in pattern:
            # Handle glob patterns
            matched_files = glob.glob(pattern)
            files.extend([Path(f) for f in matched_files])
        else:
            # Handle direct file paths
            path = Path(pattern)
            if path.exists():
                files.append(path)
            else:
                logger.warning(f"File not found: {pattern}")
    
    # Filter for PDF files only
    pdf_files = [f for f in files if f.suffix.lower() == '.pdf' and f.is_file()]
    
    if not pdf_files:
        logger.error("No valid PDF files found")
        sys.exit(1)
    
    return pdf_files


def check_dependencies():
    """Check and report available dependencies."""
    import platform
    
    logger.info("Checking dependencies...")
    
    if not PYPDF_AVAILABLE:
        logger.warning("PyPDF2/pypdf not installed. Install with: pip install PyPDF2")
    
    if not PIL_AVAILABLE:
        logger.warning("Pillow not installed. Install with: pip install Pillow")
    
    # Check for Ghostscript with platform-specific executables
    gs_found = False
    try:
        import subprocess
        
        if platform.system() == 'Windows':
            # Try different Windows Ghostscript executables
            for gs_exe in ['gswin64c', 'gswin32c', 'gs']:
                try:
                    result = subprocess.run([gs_exe, '--version'], capture_output=True, timeout=10)
                    if result.returncode == 0:
                        logger.info(f"Ghostscript found ({gs_exe}) - advanced compression available")
                        gs_found = True
                        break
                except (FileNotFoundError, subprocess.TimeoutExpired):
                    continue
        else:
            # Unix-like systems
            result = subprocess.run(['gs', '--version'], capture_output=True, timeout=10)
            if result.returncode == 0:
                logger.info("Ghostscript found - advanced compression available")
                gs_found = True
        
        if not gs_found:
            system = platform.system()
            if system == 'Windows':
                logger.warning("Ghostscript not found. Install for better compression:")
                logger.warning("  Download from: https://www.ghostscript.com/download/gsdnld.html")
                logger.warning("  Or use chocolatey: choco install ghostscript")
                logger.warning("  Or use winget: winget install AGPL.Ghostscript")
            elif system == 'Darwin':  # macOS
                logger.warning("Ghostscript not found. Install with: brew install ghostscript")
            else:  # Linux
                logger.warning("Ghostscript not found. Install with:")
                logger.warning("  Ubuntu/Debian: sudo apt-get install ghostscript")
                logger.warning("  CentOS/RHEL: sudo yum install ghostscript")
                
    except Exception as e:
        logger.debug(f"Error checking Ghostscript: {e}")
        logger.warning("Could not check Ghostscript availability")
    
    if not PYPDF_AVAILABLE:
        logger.error("No PDF processing libraries available. Please install PyPDF2 or pypdf.")
        sys.exit(1)


def main():
    """Main function."""
    args = parse_arguments()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Check dependencies
    check_dependencies()
    
    # Expand file patterns
    input_files = expand_file_patterns(args.input)
    
    # Validate arguments
    if len(input_files) > 1 and args.output:
        logger.error("Cannot specify output file with multiple input files. Use --output-dir instead.")
        sys.exit(1)
    
    # Create compressor
    target_bytes = int(args.target_size_mb * 1024 * 1024) if getattr(args, 'target_size_mb', None) else None
    compressor = PDFCompressor(args.quality, target_size_bytes=target_bytes)
    
    try:
        if len(input_files) == 1:
            # Single file compression
            input_file = input_files[0]
            output_file = args.output
            
            if args.output_dir:
                output_file = args.output_dir / f"{input_file.stem}_compressed.pdf"
            
            success, output_path = compressor.compress_file(input_file, output_file)
            
            if success:
                logger.info(f"Successfully compressed: {output_path}")
                sys.exit(0)
            else:
                logger.error("Compression failed")
                sys.exit(1)
        
        else:
            # Batch compression
            results = compressor.compress_batch(input_files, args.output_dir)
            
            # Check if any failed
            failed_files = [input_path for success, input_path, _ in results if not success]
            
            if failed_files:
                logger.error(f"Failed to compress {len(failed_files)} files:")
                for failed_file in failed_files:
                    logger.error(f"  - {failed_file}")
                sys.exit(1)
            else:
                logger.info("All files compressed successfully!")
                sys.exit(0)
    
    except KeyboardInterrupt:
        logger.info("Compression cancelled by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

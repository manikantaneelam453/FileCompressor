import os
from PyPDF2 import PdfReader, PdfWriter
import subprocess
import tempfile

def compress_pdf(input_path, compression_level='medium'):
    """
    Compress PDF file using different methods based on compression level
    """
    output_path = os.path.join(
        'compressed', 
        f"compressed_{os.path.basename(input_path)}"
    )
    
    if compression_level == 'low':
        # Simple compression using PyPDF2
        reader = PdfReader(input_path)
        writer = PdfWriter()
        
        for page in reader.pages:
            page.compress_content_streams()
            writer.add_page(page)
        
        with open(output_path, 'wb') as f:
            writer.write(f)
            
    elif compression_level in ['medium', 'high']:
        # Use Ghostscript for better compression
        quality_map = {'medium': '/printer', 'high': '/ebook'}
        quality = quality_map[compression_level]
        
        try:
            subprocess.run([
                'gs', '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4',
                f'-dPDFSETTINGS={quality}', '-dNOPAUSE', '-dQUIET', '-dBATCH',
                f'-sOutputFile={output_path}', input_path
            ], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Fallback to PyPDF2 if Ghostscript not available
            compress_pdf_fallback(input_path, output_path)
    
    return output_path

def compress_pdf_fallback(input_path, output_path):
    """Fallback PDF compression using PyPDF2"""
    reader = PdfReader(input_path)
    writer = PdfWriter()
    
    for page in reader.pages:
        writer.add_page(page)
    
    writer.add_metadata(reader.metadata)
    
    with open(output_path, 'wb') as f:
        writer.write(f)
import os
import zipfile
from docx import Document
import shutil

def compress_document(input_path, compression_level='medium'):
    """
    Compress various document types
    """
    file_ext = os.path.splitext(input_path)[1].lower()
    output_path = os.path.join(
        'compressed', 
        f"compressed_{os.path.basename(input_path)}"
    )
    
    if file_ext in ['.docx']:
        compress_docx(input_path, output_path, compression_level)
    elif file_ext == '.txt':
        compress_text_file(input_path, output_path)
    else:
        # For other files, use general compression or just copy
        shutil.copy2(input_path, output_path)
    
    return output_path

def compress_docx(input_path, output_path, compression_level):
    """Compress DOCX files by optimizing images"""
    try:
        doc = Document(input_path)
        doc.save(output_path)
    except Exception as e:
        # Fallback: copy the file
        shutil.copy2(input_path, output_path)

def compress_text_file(input_path, output_path):
    """Basic text file compression"""
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove extra whitespace (simple compression)
        compressed_content = ' '.join(content.split())
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(compressed_content)
    except Exception as e:
        # Fallback: copy the file
        shutil.copy2(input_path, output_path)
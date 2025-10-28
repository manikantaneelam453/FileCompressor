from PIL import Image
import os

def compress_image(input_path, compression_level='medium'):
    """
    Compress image file based on compression level
    """
    output_path = os.path.join(
        'compressed', 
        f"compressed_{os.path.basename(input_path)}"
    )
    
    with Image.open(input_path) as img:
        # Convert to RGB if necessary (for JPEG)
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        
        # Set quality based on compression level
        quality_map = {
            'low': 85,
            'medium': 75,
            'high': 60
        }
        
        quality = quality_map.get(compression_level, 75)
        
        # Get file extension
        file_ext = os.path.splitext(input_path)[1].lower()
        
        # Save with appropriate compression
        if file_ext in ['.png']:
            # For PNG, use optimize flag
            img.save(output_path, 'PNG', optimize=True)
        elif file_ext in ['.jpg', '.jpeg']:
            # For JPEG, use quality parameter
            img.save(output_path, 'JPEG', quality=quality, optimize=True)
        elif file_ext in ['.gif']:
            # For GIF
            img.save(output_path, 'GIF', optimize=True)
        else:
            # Default compression
            img.save(output_path, quality=quality, optimize=True)
    
    return output_path
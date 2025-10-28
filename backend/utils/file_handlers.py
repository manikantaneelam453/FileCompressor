import os
import magic

def get_file_type(file_path):
    """Get file type using python-magic"""
    try:
        file_type = magic.from_file(file_path, mime=True)
        return file_type
    except:
        # Fallback to extension-based detection
        ext = os.path.splitext(file_path)[1].lower()
        return ext

def format_file_size(size_bytes):
    """Convert bytes to human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names)-1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.2f} {size_names[i]}"

def cleanup_old_files(directory, max_age_hours=24):
    """Clean up files older than specified hours"""
    import time
    current_time = time.time()
    
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            # Check if file is older than max_age_hours
            if current_time - os.path.getctime(file_path) > max_age_hours * 3600:
                os.remove(file_path)
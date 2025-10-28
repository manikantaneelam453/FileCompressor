from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import uuid
from werkzeug.utils import secure_filename
from compression.pdf_compressor import compress_pdf
from compression.image_compressor import compress_image
from compression.document_compressor import compress_document

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
COMPRESSED_FOLDER = 'compressed'
ALLOWED_EXTENSIONS = {
    'pdf', 'jpg', 'jpeg', 'png', 'gif', 'bmp', 
    'doc', 'docx', 'txt', 'rtf'
}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['COMPRESSED_FOLDER'] = COMPRESSED_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(COMPRESSED_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/compress', methods=['POST'])
def compress_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    compression_level = request.form.get('compression_level', 'medium')
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        # Generate unique filename
        file_id = str(uuid.uuid4())
        original_ext = file.filename.rsplit('.', 1)[1].lower()
        original_filename = f"{file_id}.{original_ext}"
        compressed_filename = f"{file_id}_compressed.{original_ext}"
        
        # Save original file
        original_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
        file.save(original_path)
        
        try:
            # Compress based on file type
            if original_ext in ['pdf']:
                output_path = compress_pdf(original_path, compression_level)
            elif original_ext in ['jpg', 'jpeg', 'png', 'gif', 'bmp']:
                output_path = compress_image(original_path, compression_level)
            else:
                output_path = compress_document(original_path, compression_level)
            
            # Calculate compression stats
            original_size = os.path.getsize(original_path)
            compressed_size = os.path.getsize(output_path)
            compression_ratio = ((original_size - compressed_size) / original_size) * 100
            
            return jsonify({
                'success': True,
                'original_size': original_size,
                'compressed_size': compressed_size,
                'compression_ratio': round(compression_ratio, 2),
                'download_url': f'/download/{os.path.basename(output_path)}'
            })
            
        except Exception as e:
            return jsonify({'error': f'Compression failed: {str(e)}'}), 500
        finally:
            # Clean up original file
            if os.path.exists(original_path):
                os.remove(original_path)
    
    return jsonify({'error': 'File type not allowed'}), 400

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(
        os.path.join(app.config['COMPRESSED_FOLDER'], filename),
        as_attachment=True,
        download_name=f"compressed_{filename}"
    )

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
class FileCompressor {
    constructor() {
        this.uploadArea = document.getElementById('uploadArea');
        this.fileInput = document.getElementById('fileInput');
        this.fileList = document.getElementById('fileList');
        this.progressArea = document.getElementById('progressArea');
        this.progressFill = document.getElementById('progressFill');
        this.progressText = document.getElementById('progressText');
        this.results = document.getElementById('results');
        this.resultDetails = document.getElementById('resultDetails');
        this.downloadBtn = document.getElementById('downloadBtn');
        this.compressionLevel = document.getElementById('compressionLevel');
        
        this.selectedFile = null;
        this.currentResult = null;
        
        this.initEventListeners();
    }
    
    initEventListeners() {
        // Drag and drop events
        this.uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            this.uploadArea.classList.add('dragover');
        });
        
        this.uploadArea.addEventListener('dragleave', () => {
            this.uploadArea.classList.remove('dragover');
        });
        
        this.uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            this.uploadArea.classList.remove('dragover');
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                this.handleFileSelect(files[0]);
            }
        });
        
        // File input change
        this.fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                this.handleFileSelect(e.target.files[0]);
            }
        });
        
        // Download button
        this.downloadBtn.addEventListener('click', () => {
            if (this.currentResult) {
                this.downloadFile(this.currentResult.download_url);
            }
        });
    }
    
    handleFileSelect(file) {
        if (!this.isValidFileType(file)) {
            alert('Please select a valid file type (PDF, JPG, PNG, GIF, DOC, DOCX, TXT)');
            return;
        }
        
        if (file.size > 50 * 1024 * 1024) {
            alert('File size must be less than 50MB');
            return;
        }
        
        this.selectedFile = file;
        this.displayFileInfo(file);
    }
    
    isValidFileType(file) {
        const allowedTypes = [
            'application/pdf',
            'image/jpeg',
            'image/jpg',
            'image/png',
            'image/gif',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'text/plain'
        ];
        
        const fileExtension = file.name.split('.').pop().toLowerCase();
        const allowedExtensions = ['pdf', 'jpg', 'jpeg', 'png', 'gif', 'doc', 'docx', 'txt', 'rtf'];
        
        return allowedTypes.includes(file.type) || allowedExtensions.includes(fileExtension);
    }
    
    displayFileInfo(file) {
        this.fileList.innerHTML = `
            <div class="file-item">
                <div class="file-info">
                    <div class="file-name">
                        ${file.name}
                        <span class="file-type-badge">${this.getFileType(file)}</span>
                    </div>
                    <div class="file-size">Size: ${this.formatFileSize(file.size)}</div>
                </div>
                <button class="remove-btn" onclick="compressor.removeFile()">Remove</button>
                <button class="browse-btn" onclick="compressor.compressFile()" style="margin-left: 10px;">Compress</button>
            </div>
        `;
    }
    
    getFileType(file) {
        const extension = file.name.split('.').pop().toLowerCase();
        const typeMap = {
            'pdf': 'PDF',
            'jpg': 'JPEG',
            'jpeg': 'JPEG',
            'png': 'PNG',
            'gif': 'GIF',
            'doc': 'DOC',
            'docx': 'DOCX',
            'txt': 'TEXT',
            'rtf': 'RTF'
        };
        return typeMap[extension] || 'FILE';
    }
    
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    removeFile() {
        this.selectedFile = null;
        this.fileList.innerHTML = '';
        this.fileInput.value = '';
    }
    
    async compressFile() {
        if (!this.selectedFile) {
            alert('Please select a file first');
            return;
        }
        
        this.showProgress();
        
        const formData = new FormData();
        formData.append('file', this.selectedFile);
        formData.append('compression_level', this.compressionLevel.value);
        
        try {
            const response = await fetch('http://localhost:5000/compress', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.showResults(result);
                this.currentResult = result;
            } else {
                throw new Error(result.error);
            }
            
        } catch (error) {
            this.hideProgress();
            alert('Compression failed: ' + error.message);
            console.error('Compression error:', error);
        }
    }
    
    showProgress() {
        this.progressArea.style.display = 'block';
        this.results.style.display = 'none';
        
        // Simulate progress animation
        let progress = 0;
        const interval = setInterval(() => {
            progress += Math.random() * 10;
            if (progress >= 90) {
                clearInterval(interval);
            }
            this.progressFill.style.width = `${progress}%`;
        }, 200);
    }
    
    hideProgress() {
        this.progressArea.style.display = 'none';
        this.progressFill.style.width = '0%';
    }
    
    showResults(result) {
        this.hideProgress();
        
        const originalSize = this.formatFileSize(result.original_size);
        const compressedSize = this.formatFileSize(result.compressed_size);
        const ratio = result.compression_ratio;
        
        let ratioClass = 'compression-poor';
        if (ratio >= 30) ratioClass = 'compression-good';
        else if (ratio >= 10) ratioClass = 'compression-medium';
        
        this.resultDetails.innerHTML = `
            <div class="result-details">
                <div class="detail-item">
                    <span>Original Size:</span>
                    <span>${originalSize}</span>
                </div>
                <div class="detail-item">
                    <span>Compressed Size:</span>
                    <span>${compressedSize}</span>
                </div>
                <div class="detail-item">
                    <span>Compression Ratio:</span>
                    <span class="${ratioClass}">${ratio}% smaller</span>
                </div>
                <div class="detail-item">
                    <span>Space Saved:</span>
                    <span>${this.formatFileSize(result.original_size - result.compressed_size)}</span>
                </div>
            </div>
        `;
        
        this.results.style.display = 'block';
    }
    
    downloadFile(downloadUrl) {
        const fullUrl = `http://localhost:5000${downloadUrl}`;
        window.open(fullUrl, '_blank');
    }
}

// Initialize the compressor when page loads
document.addEventListener('DOMContentLoaded', () => {
    window.compressor = new FileCompressor();
});
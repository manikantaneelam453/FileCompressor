# 🗜️ FileCompressor - Universal File Compression Tool

![FileCompressor](https://img.shields.io/badge/FileCompressor-v1.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![Flask](https://img.shields.io/badge/Flask-2.3.3-lightgrey)
![Platform](https://img.shields.io/badge/Platform-Windows-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

A powerful, user-friendly application for compressing PDFs, images, and documents with a beautiful web interface and one-click deployment.

## ✨ Features

### 🎯 Core Functionality
- **PDF Compression** - Smart compression with multiple quality levels
- **Image Optimization** - JPEG, PNG, GIF compression with quality control
- **Document Support** - DOCX, TXT file optimization
- **Drag & Drop Interface** - Modern, intuitive web UI
- **Real-time Progress** - Live compression statistics

### 🚀 User Experience
- **One-Click Launcher** - No installation required
- **Portable** - Runs anywhere without setup
- **Multiple Compression Levels** - Low, Medium, High quality settings
- **Compression Analytics** - Before/after size comparison

## 🎮 Quick Start

### For End Users (Windows):
1. **Download** the latest release or clone this repository
2. **Double-click** `FileCompressorLauncher.bat`
3. **Open your browser** to `http://localhost:8000`
4. **Start compressing files!** 🎉

### For Developers:
```bash
# Clone the repository
git clone https://github.com/yourusername/FileCompressor.git
cd FileCompressor

# Install dependencies
cd backend
pip install -r requirements.txt

# Start the application
python app.py
# In new terminal:
cd ../frontend
python -m http.server 8000

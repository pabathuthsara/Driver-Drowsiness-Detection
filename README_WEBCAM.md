# Driver Drowsiness Detection - Webcam Version

A real-time driver drowsiness detection system using your computer's built-in webcam. This version works with any PC that has a webcam - no OBS or virtual camera setup required.

## Features

- 🎥 **Real-time face detection** using MediaPipe
- 👁️ **Blink detection** with eye aspect ratio calculation
- 😴 **Yawn detection** with mouth aspect ratio calculation
- 📊 **Live statistics** showing blink and yawn counts
- 🖼️ **Screenshot capture** with 'S' key
- 🔄 **Counter reset** with 'R' key

## Requirements

- Python 3.7 or higher
- Built-in webcam or USB webcam
- Linux/Windows/macOS

## Quick Setup

### 1. Clone or download the project
```bash
git clone <repository-url>
cd Driver-Drowsiness-Detection
```

### 2. Run the setup script
```bash
chmod +x setup_webcam.sh
./setup_webcam.sh
```

### 3. Run the application
```bash
source venv/bin/activate
python webcam_test.py
```

## Manual Setup

If you prefer manual setup:

### 1. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the application
```bash
python webcam_test.py
```

## Usage

1. **Start the application**: `python webcam_test.py`
2. **Position yourself** in front of the webcam
3. **Blink normally** to test blink detection
4. **Yawn** to test yawn detection
5. **Controls**:
   - `ESC` - Quit the application
   - `S` - Save a screenshot
   - `R` - Reset blink/yawn counters

## Troubleshooting

### Webcam not detected
- Make sure no other application is using the webcam
- Check webcam permissions in your OS
- Try restarting the application

### Poor detection accuracy
- Ensure good lighting
- Position yourself directly in front of the camera
- Keep your face clearly visible

### Performance issues
- Close other applications using the webcam
- Reduce camera resolution if needed
- Ensure adequate system resources

## Dependencies

The main dependencies are:
- `mediapipe==0.10.21` - Face mesh detection
- `opencv-python==4.11.0.86` - Computer vision
- `numpy==1.26.4` - Numerical computations

## Files

- `webcam_test.py` - Main application for webcam users
- `requirements.txt` - Python dependencies
- `setup_webcam.sh` - Automated setup script
- `README_WEBCAM.md` - This file

## License

This project is open source. Feel free to modify and distribute. 
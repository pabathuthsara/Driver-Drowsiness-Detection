#!/bin/bash

# Ubuntu 22.04 LTS Setup Script for Driver Drowsiness Detection
echo "🐧 Setting up Driver Drowsiness Detection for Ubuntu 22.04 LTS..."

# Check if running on Ubuntu 22.04
if ! grep -q "22.04" /etc/os-release; then
    echo "⚠️  Warning: This script is optimized for Ubuntu 22.04 LTS"
    echo "It may work on other versions but compatibility is not guaranteed."
    echo "Continue? (y/n)"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Display system information
echo "🔍 Checking system specifications..."
UBUNTU_VERSION=$(lsb_release -d | cut -f2)
CPU_INFO=$(lscpu | grep "Model name" | cut -d: -f2 | xargs)
CPU_CORES=$(nproc)
MEMORY=$(free -h | grep Mem | awk '{print $2}')
echo "🖥️  System: $UBUNTU_VERSION"
echo "🔧 CPU: $CPU_INFO ($CPU_CORES cores)"
echo "💾 Memory: $MEMORY"

# Check for GPU
if command -v nvidia-smi &> /dev/null; then
    GPU_INFO=$(nvidia-smi --query-gpu=name --format=csv,noheader,nounits | head -n1)
    echo "🎮 GPU: $GPU_INFO"
else
    echo "🎮 GPU: No NVIDIA GPU detected"
fi

echo "=" * 60

# Update system packages
echo "📦 Updating system packages..."
sudo apt update
sudo apt upgrade -y

# Install system dependencies for Ubuntu 22.04
echo "🔧 Installing system dependencies..."

# Essential development tools
sudo apt install -y build-essential cmake pkg-config git

# Python development
sudo apt install -y python3-dev python3-pip python3-venv python3-setuptools

# OpenCV dependencies
sudo apt install -y libopencv-dev python3-opencv
sudo apt install -y libgtk-3-dev libavcodec-dev libavformat-dev libswscale-dev
sudo apt install -y libv4l-dev libxvidcore-dev libx264-dev libjpeg-dev libpng-dev libtiff-dev
sudo apt install -y gstreamer1.0-tools gstreamer1.0-plugins-base gstreamer1.0-plugins-good
sudo apt install -y gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav

# Linear algebra and scientific computing
sudo apt install -y libatlas-base-dev liblapack-dev libblas-dev libhdf5-serial-dev
sudo apt install -y libprotobuf-dev protobuf-compiler

# Audio/Video codecs (for camera support)
sudo apt install -y ubuntu-restricted-extras

# Additional multimedia libraries
sudo apt install -y ffmpeg libavcodec-extra

# Camera and video device support
sudo apt install -y v4l-utils guvcview

# Optional: NVIDIA GPU support (if GPU detected)
if command -v nvidia-smi &> /dev/null; then
    echo "🎮 Installing NVIDIA GPU support..."
    sudo apt install -y nvidia-cuda-toolkit
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip and essential tools
echo "⬆️  Upgrading pip and essential tools..."
pip install --upgrade pip setuptools wheel

# Install Python requirements
echo "📚 Installing Python dependencies..."
pip install -r requirements.txt

# Set up camera permissions
echo "📷 Setting up camera permissions..."
sudo usermod -a -G video $USER

# Create udev rule for camera access (if needed)
if [ ! -f /etc/udev/rules.d/99-camera.rules ]; then
    echo 'SUBSYSTEM=="video4linux", GROUP="video", MODE="0664"' | sudo tee /etc/udev/rules.d/99-camera.rules
    sudo udevadm control --reload-rules
fi

# Test camera availability
echo "🔍 Testing camera availability..."
python3 -c "
import cv2
print('Testing camera access...')
for i in range(5):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            print(f'✅ Camera {i}: Working ({frame.shape[1]}x{frame.shape[0]})')
        else:
            print(f'⚠️  Camera {i}: Opened but no frames')
        cap.release()
    else:
        print(f'❌ Camera {i}: Not available')
"

# Check for OBS Virtual Camera
if [ -c /dev/video10 ]; then
    echo "🎥 OBS Virtual Camera detected at /dev/video10"
else
    echo "ℹ️  No OBS Virtual Camera detected (this is normal if OBS is not running)"
fi

# Verify installation
echo "✅ Verifying installation..."
python3 -c "
try:
    import cv2, mediapipe, numpy, psutil
    print('✅ Core dependencies verified successfully')
    print(f'OpenCV version: {cv2.__version__}')
    import mediapipe as mp
    print(f'MediaPipe version: {mp.__version__}')
    print(f'NumPy version: {numpy.__version__}')
except ImportError as e:
    print(f'❌ Import error: {e}')
    exit(1)
"

# Create desktop shortcut (optional)
read -p "🖥️  Create desktop shortcut? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    DESKTOP_FILE="$HOME/Desktop/Drowsiness-Detection.desktop"
    cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Drowsiness Detection
Comment=Ubuntu 22.04 Driver Drowsiness Detection System
Exec=bash -c "cd $(pwd) && source venv/bin/activate && python3 drowsiness_detection_ubuntu.py"
Icon=applications-multimedia
Terminal=true
Categories=Multimedia;AudioVideo;
EOF
    chmod +x "$DESKTOP_FILE"
    echo "✅ Desktop shortcut created"
fi

echo ""
echo "✅ Ubuntu 22.04 setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Log out and log back in (for camera permissions)"
echo "2. Activate environment: source venv/bin/activate"
echo "3. Run the application: python3 drowsiness_detection_ubuntu.py"
echo ""
echo "🔧 System optimizations applied:"
echo "- Camera permissions configured"
echo "- GPU support enabled (if available)"
echo "- Multimedia codecs installed"
echo "- Virtual environment created with optimized packages"
echo ""
echo "📷 Camera setup:"
echo "- Built-in camera: Usually /dev/video0"
echo "- USB webcam: Usually /dev/video1 or /dev/video2"
echo "- OBS Virtual Camera: Usually /dev/video10 (if running)"
echo ""
echo "🚀 Performance tips:"
echo "- Close unnecessary applications for better performance"
echo "- Ensure good lighting for better face detection"
echo "- Use 'htop' to monitor system resources"
echo "- Consider using dedicated GPU if available"
echo ""
echo "🔧 Troubleshooting:"
echo "- Camera issues: Run 'v4l2-ctl --list-devices'"
echo "- Permission issues: Run 'groups' to check video group membership"
echo "- Performance issues: Monitor with 'htop' and 'nvidia-smi' (if GPU)"

# Final system check
echo ""
echo "📊 Final System Check:"
echo "Python version: $(python3 --version)"
echo "Pip version: $(pip --version)"
echo "OpenCV build info:"
python3 -c "import cv2; print(cv2.getBuildInformation())" | grep -E "(CPU|GPU|Video)" 
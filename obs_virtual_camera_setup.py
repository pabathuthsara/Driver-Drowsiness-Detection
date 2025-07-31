#!/usr/bin/env python3
import subprocess
import os
import sys

def check_system_status():
    print("🔍 Checking system status for OBS Virtual Camera...")
    print("=" * 50)
    
    # Check if OBS is running
    print("1. Checking if OBS is running...")
    try:
        result = subprocess.run(['pgrep', 'obs'], capture_output=True, text=True)
        if result.returncode == 0:
            print("   ✅ OBS is running")
        else:
            print("   ❌ OBS is not running")
            print("   Please start OBS Studio first")
            return False
    except FileNotFoundError:
        print("   ❌ OBS not found. Please install OBS Studio")
        return False
    
    # Check for video devices
    print("\n2. Checking for video devices...")
    video_devices = []
    for i in range(20):
        if os.path.exists(f"/dev/video{i}"):
            video_devices.append(f"/dev/video{i}")
    
    if video_devices:
        print(f"   ✅ Found video devices: {', '.join(video_devices)}")
    else:
        print("   ❌ No video devices found")
    
    # Check v4l2loopback module
    print("\n3. Checking v4l2loopback module...")
    try:
        result = subprocess.run(['lsmod'], capture_output=True, text=True)
        if 'v4l2loopback' in result.stdout:
            print("   ✅ v4l2loopback module is loaded")
        else:
            print("   ❌ v4l2loopback module is not loaded")
            print("   This is needed for OBS Virtual Camera")
    except:
        print("   ⚠️  Could not check module status")
    
    return True

def provide_setup_instructions():
    print("\n📋 OBS Virtual Camera Setup Instructions:")
    print("=" * 50)
    print("""
1. **Start OBS Studio** (if not already running)
   - Open OBS Studio from your applications menu

2. **Add DroidCam as a source**:
   - In OBS, click the '+' button in the Sources panel
   - Select 'Video Capture Device' or 'DroidCam'
   - Choose your DroidCam source
   - Click 'OK'

3. **Start Virtual Camera**:
   - In OBS, go to 'Tools' menu
   - Select 'Start Virtual Camera'
   - You should see a green indicator when it's running

4. **Alternative: Use OBS Virtual Camera plugin**:
   - If the above doesn't work, you might need to install the OBS Virtual Camera plugin
   - Go to Tools → Virtual Camera in OBS

5. **Check if virtual camera is working**:
   - Run this script again after starting virtual camera
   - Or try: ls -la /dev/video*

6. **If v4l2loopback module fails to load**:
   - Try: sudo modprobe v4l2loopback video_nr=10
   - If that fails, you might need to disable secure boot in BIOS
   - Or try: sudo modprobe v4l2loopback exclusive_caps=1 video_nr=10
""")

def test_camera_after_setup():
    print("\n🧪 Testing camera access after setup...")
    print("=" * 50)
    
    import cv2
    
    # Try to find any working camera
    for i in range(10):
        print(f"Testing camera index {i}...")
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print(f"✅ SUCCESS! Camera {i} is working!")
                print(f"   Frame size: {frame.shape}")
                cap.release()
                return i
            cap.release()
        else:
            print(f"   Camera {i} not available")
    
    print("❌ No cameras found. Please follow the setup instructions above.")
    return None

if __name__ == "__main__":
    print("🎥 OBS Virtual Camera Setup Helper")
    print("=" * 50)
    
    # Check current status
    status_ok = check_system_status()
    
    # Provide instructions
    provide_setup_instructions()
    
    # Ask user if they want to test after setup
    print("\n" + "=" * 50)
    response = input("Have you completed the setup steps? (y/n): ").lower().strip()
    
    if response in ['y', 'yes']:
        camera_idx = test_camera_after_setup()
        if camera_idx is not None:
            print(f"\n🎉 Great! Camera {camera_idx} is working!")
            print(f"You can now use camera index {camera_idx} in your main script.")
            print("\nTo update your test.py, change the camera index to:", camera_idx)
        else:
            print("\n❌ Camera still not working. Please check:")
            print("- OBS Virtual Camera is started")
            print("- DroidCam is properly connected")
            print("- Try restarting OBS and virtual camera")
    else:
        print("\nPlease follow the setup instructions and run this script again.") 
import cv2
import sys
import os

def test_camera_access():
    print("Testing different camera access methods...")
    
    # Method 1: Try different camera indices with different backends
    backends = [cv2.CAP_ANY, cv2.CAP_V4L2, cv2.CAP_V4L, cv2.CAP_FFMPEG]
    backend_names = ["ANY", "V4L2", "V4L", "FFMPEG"]
    
    for backend_idx, backend in enumerate(backends):
        print(f"\nTrying backend: {backend_names[backend_idx]}")
        for idx in range(10):
            print(f"  Testing camera index {idx}...")
            cap = cv2.VideoCapture(idx, backend)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    print(f"    SUCCESS: Camera {idx} works with {backend_names[backend_idx]} backend!")
                    print(f"    Frame size: {frame.shape}")
                    cap.release()
                    return idx, backend
                else:
                    print(f"    Camera {idx} opened but can't read frames")
                cap.release()
            else:
                print(f"    Camera {idx} not available")
    
    # Method 2: Try specific device paths
    print("\nTrying specific device paths...")
    device_paths = [
        "/dev/video0", "/dev/video1", "/dev/video2", "/dev/video3",
        "/dev/video10", "/dev/video11", "/dev/video12",
        "/dev/dri/card0", "/dev/dri/card1"
    ]
    
    for path in device_paths:
        if os.path.exists(path):
            print(f"  Device {path} exists, trying to open...")
            cap = cv2.VideoCapture(path)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    print(f"    SUCCESS: {path} works!")
                    print(f"    Frame size: {frame.shape}")
                    cap.release()
                    return path, cv2.CAP_ANY
                cap.release()
    
    # Method 3: Try with different resolutions
    print("\nTrying with different resolutions...")
    for idx in range(5):
        cap = cv2.VideoCapture(idx)
        if cap.isOpened():
            # Try different resolutions
            resolutions = [(640, 480), (1280, 720), (1920, 1080)]
            for width, height in resolutions:
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
                ret, frame = cap.read()
                if ret:
                    print(f"    SUCCESS: Camera {idx} works at {width}x{height}")
                    print(f"    Frame size: {frame.shape}")
                    cap.release()
                    return idx, cv2.CAP_ANY
            cap.release()
    
    print("\nNo cameras found with any method.")
    return None, None

if __name__ == "__main__":
    camera_idx, backend = test_camera_access()
    if camera_idx is not None:
        print(f"\n🎉 Camera found! Index: {camera_idx}, Backend: {backend}")
        print("You can now use this camera index in your main script.")
    else:
        print("\n❌ No cameras found. Please check:")
        print("1. OBS Virtual Camera is started")
        print("2. DroidCam is properly connected")
        print("3. Virtual camera is enabled in OBS") 
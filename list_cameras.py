import cv2

def list_cameras():
    """List all available cameras"""
    print("🔍 Scanning for available cameras...")
    print("=" * 40)
    
    available_cameras = []
    
    for i in range(15):  # Check cameras 0-14
        print(f"Checking camera {i}...", end=" ")
        
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            # Get camera info
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            
            print(f"✅ Available - {width}x{height} @ {fps:.1f} FPS")
            available_cameras.append(i)
            cap.release()
        else:
            print("❌ Not available")
    
    print("\n" + "=" * 40)
    print("📋 SUMMARY")
    print("=" * 40)
    
    if available_cameras:
        print(f"Found {len(available_cameras)} camera(s):")
        for cam in available_cameras:
            print(f"  📹 Camera {cam}")
    else:
        print("❌ No cameras found!")
    
    return available_cameras

if __name__ == "__main__":
    cameras = list_cameras() 
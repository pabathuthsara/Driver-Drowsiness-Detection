import cv2
import numpy as np
import time

def quick_virtual_camera_test():
    """Quick test to find the OBS virtual camera"""
    print("🔍 Quick Virtual Camera Detection")
    print("This will test cameras 0-10 for static images")
    print()
    
    results = []
    
    for camera_index in range(11):  # Test cameras 0-10
        print(f"Testing camera {camera_index}...", end=" ")
        
        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            print("❌ Not available")
            continue
        
        # Set properties
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Capture a few frames and compare
        frames = []
        similarities = []
        
        for i in range(10):  # Capture 10 frames
            ret, frame = cap.read()
            if ret:
                frames.append(frame)
                time.sleep(0.1)
        
        cap.release()
        
        if len(frames) < 2:
            print("❌ No frames captured")
            continue
        
        # Calculate similarity between consecutive frames
        for i in range(1, len(frames)):
            # Convert to grayscale
            gray1 = cv2.cvtColor(frames[i-1], cv2.COLOR_BGR2GRAY)
            gray2 = cv2.cvtColor(frames[i], cv2.COLOR_BGR2GRAY)
            
            # Calculate similarity
            mse = np.mean((gray1.astype(float) - gray2.astype(float)) ** 2)
            max_mse = 255 ** 2
            similarity = 1 - (mse / max_mse)
            similarities.append(similarity)
        
        avg_similarity = np.mean(similarities)
        is_static = avg_similarity > 0.95  # High threshold for static detection
        
        status = "🟢 STATIC (Virtual Camera)" if is_static else "🔴 DYNAMIC (Real Camera)"
        print(f"{status} (similarity: {avg_similarity:.3f})")
        
        results.append({
            'index': camera_index,
            'is_static': is_static,
            'similarity': avg_similarity
        })
    
    print("\n" + "=" * 40)
    print("📋 RESULTS")
    print("=" * 40)
    
    virtual_cameras = []
    for result in results:
        if result['is_static']:
            virtual_cameras.append(result['index'])
            print(f"🎯 Camera {result['index']}: VIRTUAL CAMERA (similarity: {result['similarity']:.3f})")
        else:
            print(f"📹 Camera {result['index']}: Real Camera (similarity: {result['similarity']:.3f})")
    
    if virtual_cameras:
        print(f"\n💡 RECOMMENDATION:")
        print(f"   Use camera {virtual_cameras[0]} for your drowsiness detection")
        print(f"   This appears to be the OBS Virtual Camera")
    else:
        print(f"\n⚠️  No virtual camera detected")
        print(f"   Make sure OBS Virtual Camera is running with a static image")

def test_specific_camera(camera_index):
    """Test a specific camera interactively"""
    print(f"🎥 Testing Camera {camera_index}")
    print("Press 'q' to quit, 's' to save frame")
    
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print(f"❌ Could not open camera {camera_index}")
        return
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Add info to frame
        cv2.putText(frame, f'Camera {camera_index}', (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, 'Press q to quit, s to save', (10, 70), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        cv2.imshow(f'Camera {camera_index}', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            filename = f"camera_{camera_index}_{int(time.time())}.jpg"
            cv2.imwrite(filename, frame)
            print(f"📸 Saved: {filename}")
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    print("🎯 Quick OBS Virtual Camera Detector")
    print("=" * 40)
    
    # Run quick test
    quick_virtual_camera_test()
    
    # Ask if user wants to test a specific camera
    print("\n" + "=" * 40)
    response = input("🤔 Test a specific camera interactively? (enter camera number or 'n'): ")
    
    if response.isdigit():
        camera_index = int(response)
        test_specific_camera(camera_index)
    else:
        print("👋 Goodbye!") 
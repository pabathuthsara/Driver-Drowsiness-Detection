import cv2
import numpy as np
import time

def test_camera_10():
    """Test camera 10 to see if it's the OBS virtual camera"""
    print("🔍 Testing Camera 10 for OBS Virtual Camera")
    print("=" * 50)
    
    cap = cv2.VideoCapture(10)
    if not cap.isOpened():
        print("❌ Could not open camera 10")
        return
    
    print("✅ Camera 10 opened successfully")
    
    # Set properties
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    print("📸 Capturing frames to analyze...")
    
    # Capture frames and analyze
    frames = []
    similarities = []
    
    for i in range(20):  # Capture 20 frames
        ret, frame = cap.read()
        if ret:
            frames.append(frame)
            print(f"  Frame {i+1}/20 captured")
            time.sleep(0.1)
        else:
            print(f"  ❌ Failed to capture frame {i+1}")
    
    cap.release()
    
    if len(frames) < 2:
        print("❌ Not enough frames captured")
        return
    
    print(f"\n🔍 Analyzing {len(frames)} frames...")
    
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
    min_similarity = np.min(similarities)
    max_similarity = np.max(similarities)
    
    print(f"\n📊 ANALYSIS RESULTS:")
    print(f"  Average Similarity: {avg_similarity:.4f}")
    print(f"  Min Similarity: {min_similarity:.4f}")
    print(f"  Max Similarity: {max_similarity:.4f}")
    print(f"  Frames Analyzed: {len(similarities)}")
    
    # Determine if it's static
    is_static = avg_similarity > 0.95
    
    print(f"\n🎯 CONCLUSION:")
    if is_static:
        print(f"  🟢 STATIC IMAGE DETECTED!")
        print(f"  📹 Camera 10 is likely the OBS Virtual Camera")
        print(f"  💡 Use camera index 10 in your drowsiness detection system")
    else:
        print(f"  🔴 DYNAMIC CONTENT DETECTED")
        print(f"  📹 Camera 10 appears to be a real camera")
    
    # Save a sample frame
    if frames:
        filename = "camera_10_sample.jpg"
        cv2.imwrite(filename, frames[-1])
        print(f"\n📸 Sample frame saved as: {filename}")
    
    return is_static, avg_similarity

if __name__ == "__main__":
    test_camera_10() 
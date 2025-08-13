import cv2
import numpy as np
import time
import sys
from typing import List, Tuple, Optional

class VirtualCameraDetector:
    def __init__(self):
        self.max_cameras_to_test = 10
        self.test_duration = 3  # seconds to test each camera
        self.frame_analysis_count = 30  # number of frames to analyze for each camera
        self.similarity_threshold = 0.98  # threshold for considering frames similar (static image)
        
    def list_available_cameras(self) -> List[int]:
        """Find all available camera indices"""
        available_cameras = []
        
        print("🔍 Scanning for available cameras...")
        for i in range(self.max_cameras_to_test):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                # Get camera info
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                fps = cap.get(cv2.CAP_PROP_FPS)
                
                print(f"📹 Camera {i}: {width}x{height} @ {fps:.1f} FPS")
                available_cameras.append(i)
                cap.release()
            else:
                print(f"❌ Camera {i}: Not available")
                
        return available_cameras
    
    def get_camera_name(self, camera_index: int) -> str:
        """Try to get camera name/description"""
        cap = cv2.VideoCapture(camera_index)
        if cap.isOpened():
            # Try to get camera name (this might not work on all systems)
            name = cap.getBackendName()
            cap.release()
            return name
        return "Unknown"
    
    def calculate_frame_similarity(self, frame1: np.ndarray, frame2: np.ndarray) -> float:
        """Calculate similarity between two frames"""
        # Convert to grayscale for comparison
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        
        # Calculate structural similarity index
        # For simplicity, we'll use mean squared error
        mse = np.mean((gray1.astype(float) - gray2.astype(float)) ** 2)
        max_mse = 255 ** 2
        similarity = 1 - (mse / max_mse)
        
        return similarity
    
    def analyze_camera_feed(self, camera_index: int) -> Tuple[bool, float, List[float], Optional[np.ndarray]]:
        """Analyze a camera feed to determine if it's showing a static image"""
        cap = cv2.VideoCapture(camera_index)
        
        if not cap.isOpened():
            return False, 0.0, [], None
        
        # Set camera properties
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        frames = []
        similarities = []
        last_frame = None
        
        print(f"🔍 Testing camera {camera_index} for {self.test_duration} seconds...")
        start_time = time.time()
        
        while time.time() - start_time < self.test_duration and len(frames) < self.frame_analysis_count:
            ret, frame = cap.read()
            if ret:
                frames.append(frame)
                
                if last_frame is not None:
                    similarity = self.calculate_frame_similarity(last_frame, frame)
                    similarities.append(similarity)
                
                last_frame = frame.copy()
            
            time.sleep(0.1)  # Small delay to avoid overwhelming the camera
        
        cap.release()
        
        if len(similarities) == 0:
            return False, 0.0, similarities, None
        
        avg_similarity = np.mean(similarities)
        is_static = avg_similarity > self.similarity_threshold
        
        return is_static, avg_similarity, similarities, frames[-1] if frames else None
    
    def detect_virtual_camera(self) -> Optional[int]:
        """Main function to detect which camera is the OBS virtual camera"""
        print("🚀 Starting Virtual Camera Detection...")
        print("=" * 50)
        
        # Find available cameras
        available_cameras = self.list_available_cameras()
        
        if not available_cameras:
            print("❌ No cameras found!")
            return None
        
        print(f"\n📊 Found {len(available_cameras)} camera(s)")
        print("=" * 50)
        
        # Test each camera
        camera_results = []
        
        for camera_index in available_cameras:
            print(f"\n🔍 Testing Camera {camera_index}...")
            
            is_static, avg_similarity, similarities, sample_frame = self.analyze_camera_feed(camera_index)
            
            result = {
                'index': camera_index,
                'is_static': is_static,
                'avg_similarity': avg_similarity,
                'similarities': similarities,
                'sample_frame': sample_frame
            }
            
            camera_results.append(result)
            
            status = "🟢 STATIC (Likely Virtual Camera)" if is_static else "🔴 DYNAMIC (Real Camera)"
            print(f"   {status}")
            print(f"   Average Similarity: {avg_similarity:.4f}")
            print(f"   Frames Analyzed: {len(similarities)}")
        
        # Find the most likely virtual camera
        virtual_camera = None
        max_similarity = 0
        
        for result in camera_results:
            if result['is_static'] and result['avg_similarity'] > max_similarity:
                virtual_camera = result['index']
                max_similarity = result['avg_similarity']
        
        # Display results
        print("\n" + "=" * 50)
        print("📋 ANALYSIS RESULTS")
        print("=" * 50)
        
        for result in camera_results:
            status = "🟢 VIRTUAL CAMERA" if result['is_static'] else "🔴 REAL CAMERA"
            print(f"Camera {result['index']}: {status}")
            print(f"  - Average Similarity: {result['avg_similarity']:.4f}")
            print(f"  - Frames Analyzed: {len(result['similarities'])}")
            
            if result['sample_frame'] is not None:
                # Save sample frame
                filename = f"camera_{result['index']}_sample.jpg"
                cv2.imwrite(filename, result['sample_frame'])
                print(f"  - Sample frame saved: {filename}")
        
        if virtual_camera is not None:
            print(f"\n🎯 DETECTED VIRTUAL CAMERA: Camera {virtual_camera}")
            print(f"   This camera shows a static image (similarity: {max_similarity:.4f})")
            print(f"   It's likely the OBS Virtual Camera with a static image feed")
        else:
            print(f"\n⚠️  No virtual camera detected")
            print(f"   All cameras appear to be showing dynamic content")
        
        return virtual_camera
    
    def interactive_test(self, camera_index: int):
        """Interactive test for a specific camera"""
        cap = cv2.VideoCapture(camera_index)
        
        if not cap.isOpened():
            print(f"❌ Could not open camera {camera_index}")
            return
        
        print(f"🎥 Interactive test for Camera {camera_index}")
        print("Press 'q' to quit, 's' to save frame")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Add camera info to frame
            cv2.putText(frame, f'Camera {camera_index}', (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, 'Press q to quit, s to save', (10, 70), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            cv2.imshow(f'Camera {camera_index} Test', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                filename = f"camera_{camera_index}_interactive_{int(time.time())}.jpg"
                cv2.imwrite(filename, frame)
                print(f"📸 Saved: {filename}")
        
        cap.release()
        cv2.destroyAllWindows()

def main():
    detector = VirtualCameraDetector()
    
    print("🎯 OBS Virtual Camera Detector")
    print("This tool helps identify which camera is the OBS Virtual Camera")
    print("by detecting static images (like a picture you've added to OBS)")
    print()
    
    # Detect virtual camera
    virtual_camera = detector.detect_virtual_camera()
    
    if virtual_camera is not None:
        print(f"\n💡 RECOMMENDATION:")
        print(f"   Use camera index {virtual_camera} in your drowsiness detection system")
        print(f"   This appears to be the OBS Virtual Camera")
        
        # Ask if user wants interactive test
        response = input(f"\n🤔 Would you like to do an interactive test of camera {virtual_camera}? (y/n): ")
        if response.lower() in ['y', 'yes']:
            detector.interactive_test(virtual_camera)
    else:
        print(f"\n💡 RECOMMENDATION:")
        print(f"   No virtual camera detected. You may need to:")
        print(f"   1. Start OBS Studio")
        print(f"   2. Add a static image to your scene")
        print(f"   3. Start Virtual Camera in OBS")
        print(f"   4. Run this test again")

if __name__ == "__main__":
    main() 
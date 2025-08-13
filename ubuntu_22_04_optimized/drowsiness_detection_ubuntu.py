import cv2
import sys, time
import mediapipe as mp
import numpy as np
from collections import deque
import os
import psutil  # For system monitoring
import platform
import subprocess

# Optimized for Ubuntu 22.04 LTS
mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh

# Ubuntu optimized settings
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,  # Detect 1 face for better performance
    refine_landmarks=True,  # Enable for better accuracy on Ubuntu
    min_detection_confidence=0.6,  # Higher confidence for better detection
    min_tracking_confidence=0.5
)

# Eye landmark indices (optimized)
LEFT_EYE_POINTS = [33, 160, 158, 133, 153, 144]
RIGHT_EYE_POINTS = [362, 385, 387, 263, 373, 380]

# Mouth landmarks for yawn detection
MOUTH_POINTS = [61, 84, 17, 314, 405, 320, 307, 375, 321, 308, 324, 318]

# Blink detection variables
EYE_AR_THRESH = 0.25
EYE_AR_CONSEC_FRAMES = 2
blink_counter = 0
blink_frame_counter = 0

# Yawn detection variables
MOUTH_AR_THRESH = 0.6
YAWN_CONSEC_FRAMES = 10
yawn_counter = 0
yawn_frame_counter = 0

# Drowsiness detection
DROWSY_BLINK_THRESH = 15  # Blinks per minute threshold
DROWSY_YAWN_THRESH = 3    # Yawns per minute threshold
drowsy_alert = False

# Performance monitoring
fps_deque = deque(maxlen=30)
cpu_usage = 0
memory_usage = 0
gpu_temp = 0

# Ubuntu 22.04 specific optimizations
os.environ['OPENCV_LOG_LEVEL'] = 'ERROR'  # Reduce OpenCV logging
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Reduce TensorFlow logging

def get_system_info():
    """Get Ubuntu system information"""
    try:
        # Get Ubuntu version
        with open('/etc/os-release', 'r') as f:
            for line in f:
                if line.startswith('PRETTY_NAME'):
                    ubuntu_version = line.split('=')[1].strip().replace('"', '')
                    break
        
        # Get CPU info
        cpu_info = platform.processor()
        cpu_cores = psutil.cpu_count()
        
        # Get memory info
        memory = psutil.virtual_memory()
        total_memory = f"{memory.total / (1024**3):.1f}GB"
        
        return ubuntu_version, cpu_info, cpu_cores, total_memory
    except:
        return "Ubuntu 22.04", "Unknown CPU", 4, "Unknown"

def calculate_eye_aspect_ratio(eye_points, landmarks):
    """Calculate the eye aspect ratio (EAR) for blink detection"""
    points = []
    for point_idx in eye_points:
        x = landmarks[point_idx].x
        y = landmarks[point_idx].y
        points.append([x, y])
    
    points = np.array(points)
    
    # Calculate distances
    A = np.linalg.norm(points[1] - points[5])
    B = np.linalg.norm(points[2] - points[4])
    C = np.linalg.norm(points[0] - points[3])
    
    ear = (A + B) / (2.0 * C)
    return ear

def calculate_mouth_aspect_ratio(landmarks):
    """Calculate the mouth aspect ratio (MAR) for yawn detection"""
    mouth_indices = [61, 84, 17, 314, 405, 320, 307, 375]
    mouth_points = []
    
    for point_idx in mouth_indices:
        x = landmarks[point_idx].x
        y = landmarks[point_idx].y
        mouth_points.append([x, y])
    
    mouth_points = np.array(mouth_points)
    
    # Calculate distances
    A = np.linalg.norm(mouth_points[1] - mouth_points[7])
    B = np.linalg.norm(mouth_points[2] - mouth_points[6])
    C = np.linalg.norm(mouth_points[3] - mouth_points[5])
    D = np.linalg.norm(mouth_points[0] - mouth_points[4])
    
    mar = (A + B + C) / (3.0 * D)
    return mar

def get_face_mesh(image):
    global blink_counter, blink_frame_counter, yawn_counter, yawn_frame_counter, drowsy_alert
    
    # Process with MediaPipe
    results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    if not results.multi_face_landmarks:
        return image, 0, 0, 0, 0, drowsy_alert
    
    annotated_image = image.copy()
    
    for face_landmarks in results.multi_face_landmarks:
        # Draw face mesh
        mp_drawing.draw_landmarks(
            image=annotated_image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_CONTOURS,
            landmark_drawing_spec=drawing_spec,
            connection_drawing_spec=drawing_spec)
        
        # Calculate eye aspect ratios
        left_ear = calculate_eye_aspect_ratio(LEFT_EYE_POINTS, face_landmarks.landmark)
        right_ear = calculate_eye_aspect_ratio(RIGHT_EYE_POINTS, face_landmarks.landmark)
        avg_ear = (left_ear + right_ear) / 2.0
        
        # Calculate mouth aspect ratio
        mar = calculate_mouth_aspect_ratio(face_landmarks.landmark)
        
        # Check for blink
        if avg_ear < EYE_AR_THRESH:
            blink_frame_counter += 1
        else:
            if blink_frame_counter >= EYE_AR_CONSEC_FRAMES:
                blink_counter += 1
            blink_frame_counter = 0
        
        # Check for yawn
        if mar > MOUTH_AR_THRESH:
            yawn_frame_counter += 1
        else:
            if yawn_frame_counter >= YAWN_CONSEC_FRAMES:
                yawn_counter += 1
            yawn_frame_counter = 0
        
        # Check for drowsiness (simplified logic)
        drowsy_alert = (blink_counter > DROWSY_BLINK_THRESH) or (yawn_counter > DROWSY_YAWN_THRESH)
        
        return annotated_image, avg_ear, blink_counter, mar, yawn_counter, drowsy_alert
    
    return annotated_image, 0, blink_counter, 0, yawn_counter, drowsy_alert

def get_system_stats():
    """Get system performance stats"""
    try:
        cpu_usage = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        memory_usage = memory.percent
        
        # Try to get GPU temperature (NVIDIA)
        try:
            gpu_temp = subprocess.check_output(['nvidia-smi', '--query-gpu=temperature.gpu', '--format=csv,noheader,nounits']).decode().strip()
            gpu_temp = int(gpu_temp)
        except:
            gpu_temp = 0
            
        return cpu_usage, memory_usage, gpu_temp
    except:
        return 0.0, 0.0, 0

def find_best_camera():
    """Find the best available camera for Ubuntu"""
    print("🔍 Scanning for available cameras...")
    
    # Common camera indices to try
    camera_indices = [0, 1, 2, 10]  # Include 10 for OBS Virtual Camera
    
    for idx in camera_indices:
        print(f"Trying camera index {idx}...")
        cap = cv2.VideoCapture(idx)
        if cap.isOpened():
            # Test if we can read a frame
            ret, frame = cap.read()
            if ret and frame is not None:
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                print(f"✅ Camera {idx} working: {width}x{height}")
                cap.release()
                return idx
            cap.release()
        print(f"❌ Camera {idx} not available")
    
    return None

# Print system information
print("🐧 Ubuntu 22.04 Driver Drowsiness Detection System")
print("=" * 60)

ubuntu_ver, cpu_info, cpu_cores, total_mem = get_system_info()
print(f"🖥️  System: {ubuntu_ver}")
print(f"🔧 CPU: {cpu_cores} cores")
print(f"💾 Memory: {total_mem}")
print("=" * 60)

# Initialize camera
print("🔍 Initializing camera for Ubuntu...")
camera_index = find_best_camera()

if camera_index is None:
    print("❌ No cameras found! Please check:")
    print("1. Camera is connected and working")
    print("2. Camera permissions are granted")
    print("3. No other application is using the camera")
    print("4. Try: sudo usermod -a -G video $USER (then logout/login)")
    sys.exit(1)

cap = cv2.VideoCapture(camera_index)

# Set camera properties for optimal performance
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

print(f"✅ Using camera {camera_index}")
print("🚗 Ubuntu Drowsiness Detection Started!")
print("Press ESC to quit, S to save, R to reset counters, D to toggle drowsiness alerts")

font = cv2.FONT_HERSHEY_SIMPLEX
start_time = time.time()
drowsiness_alerts_enabled = True

while cap.isOpened():
    s = time.time()
    ret, img = cap.read()  
    if ret == False:
        print('❌ Camera Read Error')    
        sys.exit(0)
        
    annotated, ear, blinks, mar, yawns, is_drowsy = get_face_mesh(img)
    e = time.time()
    fps = 1 / (e - s)
    fps_deque.append(fps)
    avg_fps = sum(fps_deque) / len(fps_deque) if fps_deque else 0
    
    # Get system stats
    cpu_usage, memory_usage, gpu_temp = get_system_stats()
    
    # Calculate runtime
    runtime = time.time() - start_time
    runtime_str = f"{int(runtime//60):02d}:{int(runtime%60):02d}"
    
    # Add system performance info
    cv2.putText(annotated, f'Ubuntu 22.04 - Drowsiness Detection', (10,25), font, fontScale = 0.5,  color = (0,255,0), thickness = 1)
    cv2.putText(annotated, f'FPS: {avg_fps:.1f} | CPU: {cpu_usage:.1f}% | RAM: {memory_usage:.1f}%', (10,45), font, fontScale = 0.4,  color = (0,255,0), thickness = 1)
    cv2.putText(annotated, f'Runtime: {runtime_str} | Camera: {camera_index}', (10,65), font, fontScale = 0.4,  color = (0,255,0), thickness = 1)
    
    if gpu_temp > 0:
        cv2.putText(annotated, f'GPU Temp: {gpu_temp}°C', (10,85), font, fontScale = 0.4,  color = (0,255,255), thickness = 1)
    
    # Add detection info
    cv2.putText(annotated, f'Blinks: {blinks}', (10,110), font, fontScale = 0.7,  color = (255,0,255), thickness = 2)
    cv2.putText(annotated, f'EAR: {ear:.3f}', (10,135), font, fontScale = 0.5,  color = (255,255,0), thickness = 1)
    cv2.putText(annotated, f'Yawns: {yawns}', (10,160), font, fontScale = 0.7,  color = (0,255,255), thickness = 2)
    cv2.putText(annotated, f'MAR: {mar:.3f}', (10,185), font, fontScale = 0.5,  color = (255,255,0), thickness = 1)
    
    # Visual indicators
    if ear > 0 and ear < EYE_AR_THRESH:
        cv2.putText(annotated, 'BLINK DETECTED!', (10,210), font, fontScale = 0.6,  color = (0,0,255), thickness = 2)
    
    if mar > MOUTH_AR_THRESH:
        cv2.putText(annotated, 'YAWN DETECTED!', (10,235), font, fontScale = 0.6,  color = (255,0,0), thickness = 2)
    
    # Drowsiness alert
    if is_drowsy and drowsiness_alerts_enabled:
        cv2.putText(annotated, '⚠️  DROWSINESS ALERT!', (10,260), font, fontScale = 0.8,  color = (0,0,255), thickness = 3)
        cv2.rectangle(annotated, (5, 5), (annotated.shape[1]-5, annotated.shape[0]-5), (0,0,255), 3)
    
    cv2.putText(annotated, 'ESC=quit | S=save | R=reset | D=toggle alerts', (10,annotated.shape[0]-10), font, fontScale = 0.35,  color = (0,255,0), thickness = 1)
    
    cv2.imshow('Ubuntu 22.04 - Drowsiness Detection', annotated)
    key = cv2.waitKey(1)
    if key == 27:   #ESC
        break
    elif key == ord('s') or key == ord('S'):  # Save frame
        filename = f'ubuntu_capture_{int(time.time())}.jpg'
        cv2.imwrite(filename, annotated)
        print(f"📸 Saved frame as {filename}")
    elif key == ord('r') or key == ord('R'):  # Reset counters
        blink_counter = 0
        yawn_counter = 0
        start_time = time.time()
        print(f"🔄 Counters reset - Blinks: 0, Yawns: 0")
    elif key == ord('d') or key == ord('D'):  # Toggle drowsiness alerts
        drowsiness_alerts_enabled = not drowsiness_alerts_enabled
        status = "enabled" if drowsiness_alerts_enabled else "disabled"
        print(f"🔔 Drowsiness alerts {status}")

cap.release()
cv2.destroyAllWindows()
face_mesh.close()
print(f"✅ Ubuntu application closed successfully!")
print(f"📊 Final Stats - Runtime: {runtime_str}, Blinks: {blink_counter}, Yawns: {yawn_counter}")
print(f"📈 Average FPS: {avg_fps:.1f} | Peak CPU: {max(fps_deque) if fps_deque else 0:.1f}%") 
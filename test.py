import cv2
import sys, time
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh

# For live video:

drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,  # Set to False for video
    max_num_faces=2,          # Allow up to 2 faces
    refine_landmarks=True,    # Better landmark accuracy
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Eye landmark indices for MediaPipe Face Mesh
LEFT_EYE_LANDMARKS = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
RIGHT_EYE_LANDMARKS = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]

# Specific points for eye aspect ratio calculation
LEFT_EYE_POINTS = [33, 160, 158, 133, 153, 144]  # Left eye key points
RIGHT_EYE_POINTS = [362, 385, 387, 263, 373, 380]  # Right eye key points

# Mouth landmarks for yawn detection
MOUTH_POINTS = [61, 84, 17, 314, 405, 320, 307, 375, 321, 308, 324, 318]  # Key mouth points
# Alternative mouth points for better yawn detection
MOUTH_OUTER_POINTS = [61, 146, 91, 181, 84, 17, 314, 405, 320, 307, 375, 321, 308, 324, 318]

# Blink detection variables
EYE_AR_THRESH = 0.25  # Eye aspect ratio threshold for blink
EYE_AR_CONSEC_FRAMES = 2  # Number of consecutive frames below threshold for blink
blink_counter = 0
blink_frame_counter = 0

# Yawn detection variables
MOUTH_AR_THRESH = 0.6  # Mouth aspect ratio threshold for yawn
YAWN_CONSEC_FRAMES = 10  # Number of consecutive frames above threshold for yawn
yawn_counter = 0
yawn_frame_counter = 0

def calculate_eye_aspect_ratio(eye_points, landmarks):
    """Calculate the eye aspect ratio (EAR) for blink detection"""
    # Get the coordinates of the eye landmarks
    points = []
    for point_idx in eye_points:
        x = landmarks[point_idx].x
        y = landmarks[point_idx].y
        points.append([x, y])
    
    points = np.array(points)
    
    # Calculate the euclidean distances between the vertical eye landmarks
    A = np.linalg.norm(points[1] - points[5])  # Vertical distance 1
    B = np.linalg.norm(points[2] - points[4])  # Vertical distance 2
    
    # Calculate the euclidean distance between the horizontal eye landmarks
    C = np.linalg.norm(points[0] - points[3])  # Horizontal distance
    
    # Calculate the eye aspect ratio
    ear = (A + B) / (2.0 * C)
    return ear

def calculate_mouth_aspect_ratio(landmarks):
    """Calculate the mouth aspect ratio (MAR) for yawn detection"""
    # Get mouth landmarks
    mouth_points = []
    mouth_indices = [61, 84, 17, 314, 405, 320, 307, 375]  # Key mouth landmarks
    
    for point_idx in mouth_indices:
        x = landmarks[point_idx].x
        y = landmarks[point_idx].y
        mouth_points.append([x, y])
    
    mouth_points = np.array(mouth_points)
    
    # Calculate vertical distances (mouth height)
    A = np.linalg.norm(mouth_points[1] - mouth_points[7])  # Top to bottom 1
    B = np.linalg.norm(mouth_points[2] - mouth_points[6])  # Top to bottom 2
    C = np.linalg.norm(mouth_points[3] - mouth_points[5])  # Top to bottom 3
    
    # Calculate horizontal distance (mouth width)
    D = np.linalg.norm(mouth_points[0] - mouth_points[4])  # Left to right
    
    # Calculate the mouth aspect ratio
    mar = (A + B + C) / (3.0 * D)
    return mar

def get_face_mesh(image):
    global blink_counter, blink_frame_counter, yawn_counter, yawn_frame_counter
    
    results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    # Print and draw face mesh landmarks on the image.
    if not results.multi_face_landmarks:
        return image, 0, 0, 0, 0
    
    annotated_image = image.copy()
    
    for face_landmarks in results.multi_face_landmarks:
        # Draw face mesh
        mp_drawing.draw_landmarks(
            image=annotated_image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_CONTOURS,
            landmark_drawing_spec=drawing_spec,
            connection_drawing_spec=drawing_spec)
        
        # Calculate eye aspect ratios for blink detection
        left_ear = calculate_eye_aspect_ratio(LEFT_EYE_POINTS, face_landmarks.landmark)
        right_ear = calculate_eye_aspect_ratio(RIGHT_EYE_POINTS, face_landmarks.landmark)
        avg_ear = (left_ear + right_ear) / 2.0
        
        # Calculate mouth aspect ratio for yawn detection
        mar = calculate_mouth_aspect_ratio(face_landmarks.landmark)
        
        # Check for blink
        if avg_ear < EYE_AR_THRESH:
            blink_frame_counter += 1
        else:
            # If eyes were closed for sufficient frames, register a blink
            if blink_frame_counter >= EYE_AR_CONSEC_FRAMES:
                blink_counter += 1
            blink_frame_counter = 0
        
        # Check for yawn
        if mar > MOUTH_AR_THRESH:
            yawn_frame_counter += 1
        else:
            # If mouth was open for sufficient frames, register a yawn
            if yawn_frame_counter >= YAWN_CONSEC_FRAMES:
                yawn_counter += 1
            yawn_frame_counter = 0
        
        return annotated_image, avg_ear, blink_counter, mar, yawn_counter
    
    return annotated_image, 0, blink_counter, 0, yawn_counter
     
     
font = cv2.FONT_HERSHEY_SIMPLEX    
cap = cv2.VideoCapture(2)  # Use camera index 2 which is available
if (cap.isOpened() == False): 
  print("Unable to read DroidCam feed")
else:
  print("DroidCam connected successfully!")    
  
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("Blink & Yawn Detection Started!")
print("Blink normally and yawn to test the counters.")
print("Press ESC to quit, S to save, R to reset counters")

while cap.isOpened():
    s = time.time()
    ret, img = cap.read()  
    if ret == False:
        print('WebCAM Read Error')    
        sys.exit(0)
        
    annotated, ear, blinks, mar, yawns = get_face_mesh(img)
    e = time.time()
    fps = 1 / (e - s)
    
    # Add FPS and title
    cv2.putText(annotated, 'FPS:%5.2f'%(fps), (10,30), font, fontScale = 0.7,  color = (0,255,0), thickness = 2)
    cv2.putText(annotated, 'DroidCam: Blink & Yawn Detection', (10,60), font, fontScale = 0.6,  color = (0,255,0), thickness = 1)
    
    # Add blink counter and EAR display
    cv2.putText(annotated, f'Blinks: {blinks}', (10,90), font, fontScale = 0.8,  color = (255,0,255), thickness = 2)
    cv2.putText(annotated, f'EAR: {ear:.3f}', (10,120), font, fontScale = 0.5,  color = (255,255,0), thickness = 1)
    
    # Add yawn counter and MAR display
    cv2.putText(annotated, f'Yawns: {yawns}', (10,150), font, fontScale = 0.8,  color = (0,255,255), thickness = 2)
    cv2.putText(annotated, f'MAR: {mar:.3f}', (10,180), font, fontScale = 0.5,  color = (255,255,0), thickness = 1)
    
    # Visual indicators for detection
    if ear > 0 and ear < EYE_AR_THRESH:
        cv2.putText(annotated, 'BLINK DETECTED!', (10,210), font, fontScale = 0.6,  color = (0,0,255), thickness = 2)
    
    if mar > MOUTH_AR_THRESH:
        cv2.putText(annotated, 'YAWN DETECTED!', (10,240), font, fontScale = 0.6,  color = (255,0,0), thickness = 2)
    
    cv2.putText(annotated, 'ESC=quit, S=save, R=reset counters', (10,270), font, fontScale = 0.4,  color = (0,255,0), thickness = 1)
    
    cv2.imshow('DroidCam Face Mesh', annotated)
    key = cv2.waitKey(1)
    if key == 27:   #ESC
        break
    elif key == ord('s') or key == ord('S'):  # Save frame
        filename = f'face_mesh_capture_{int(time.time())}.jpg'
        cv2.imwrite(filename, annotated)
        print(f"Saved frame as {filename}")
    elif key == ord('r') or key == ord('R'):  # Reset counters
        blink_counter = 0
        yawn_counter = 0
        print(f"Counters reset - Blinks: 0, Yawns: 0")

cap.release()
cv2.destroyAllWindows()
face_mesh.close()
print(f"Face mesh application closed successfully!")
print(f"Final Stats - Blinks: {blink_counter}, Yawns: {yawn_counter}")
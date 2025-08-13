import cv2

def open_camera_10():
    """Simply open and display camera 10"""
    print("🎥 Opening Camera 10...")
    
    cap = cv2.VideoCapture(10)
    if not cap.isOpened():
        print("❌ Could not open camera 10")
        return
    
    print("✅ Camera 10 opened successfully!")
    print("Press 'q' to quit")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to read frame")
            break
        
        # Display the frame
        cv2.imshow('Camera 10', frame)
        
        # Check for 'q' key to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("👋 Camera 10 closed")

if __name__ == "__main__":
    open_camera_10() 
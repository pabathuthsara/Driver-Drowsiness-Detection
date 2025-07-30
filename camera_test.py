import cv2

print("Testing camera access...")
print("Trying different camera indices:")

for i in range(5):  # Test camera indices 0-4
    print(f"\nTrying camera index {i}...")
    cap = cv2.VideoCapture(i)
    
    if cap.isOpened():
        print(f"Camera {i} is available!")
        ret, frame = cap.read()
        if ret:
            print(f"Camera {i} can capture frames (resolution: {frame.shape[1]}x{frame.shape[0]})")
            # Test if we can show a window (this might fail in some environments)
            try:
                cv2.imshow(f'Camera {i} Test', frame)
                cv2.waitKey(1000)  # Show for 1 second
                cv2.destroyAllWindows()
                print(f"Camera {i} display test successful")
            except Exception as e:
                print(f"Camera {i} display failed: {e}")
        else:
            print(f"Camera {i} opened but cannot capture frames")
        cap.release()
    else:
        print(f"Camera {i} not available")

print("\nCamera test completed!")
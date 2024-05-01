
# import cv2
# from imageai.Detection import VideoObjectDetection
# import os 

# # Get the current working directory
# execution_path = os.getcwd()

# # Create a VideoCapture object to capture frames from the camera (0 is the default camera)
# cap = cv2.VideoCapture(0)

# # Check if the camera opened successfully
# if not cap.isOpened():
#     print("Error: Could not open camera")
#     exit()

# # Create an object of VideoObjectDetection
# vid_obj_detect = VideoObjectDetection()
# vid_obj_detect.setModelTypeAsYOLOv3()
# vid_obj_detect.setModelPath(r"C:\Users\USER\Desktop\QueenGambot\yolov3.pt")
# vid_obj_detect.loadModel()
# vid_obj_detect.useCPU()

# # Process frames from the camera
# while True:
#     # Capture frame-by-frame from the camera
#     ret, frame = cap.read()

#     if not ret:
#         print("Error: Could not read frame")
#         break

#     # Detect objects in the frame
#     detected_frame, detections = vid_obj_detect.detectObjectsFromVideo(camera_input=cap, frames_per_second=20, log_progress=True, minimum_percentage_probability=30,save_detected_video=False)

#     # Display the detected frame in a window
#     cv2.imshow("Detected Objects", detected_frame)

#     # Check for key press to exit
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release the VideoCapture object and close all windows
# cap.release()
# cv2.destroyAllWindows()


import cv2

# Create a VideoCapture object to capture frames from the camera (0 is the default camera)
cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera")
    exit()

while True:
    # Capture frame-by-frame from the camera
    ret, frame = cap.read()

    if not ret:
        print("Error: Could not read frame")
        break

    # Detect inner corners of the chessboard
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, inner_corners = cv2.findChessboardCorners(gray, (7, 7), None)

    # If inner corners are detected, draw them on the frame
    if ret:
        cv2.drawChessboardCorners(frame, (7, 7), inner_corners, ret)

        # Find outer corners of the chessboard
        outer_corners = cv2.boxPoints(cv2.minAreaRect(inner_corners))
        outer_corners = outer_corners.astype(int)
        
        # Draw the outer corners on the frame
        for corner in outer_corners:
            cv2.circle(frame, tuple(corner), 5, (0, 255, 0), -1)

    # Display the frame with detected corners
    cv2.imshow("Chessboard Detection", frame)

    # Check for key press to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture object and close all windows
cap.release()
cv2.destroyAllWindows()


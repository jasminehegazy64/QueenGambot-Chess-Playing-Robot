
    

# import cv2
# import numpy as np

# # Load template images for each chess piece
# template_images = {
#     'pawn': cv2.imread(r'C:\Users\USER\Desktop\QueenGambot-Chess-Playing-Robot\pieces\solder.jpeg', 0),
#     'rook': cv2.imread(r'C:\Users\USER\Desktop\QueenGambot-Chess-Playing-Robot\pieces\tabya.jpeg', 0),
#     'knight': cv2.imread(r'C:\Users\USER\Desktop\QueenGambot-Chess-Playing-Robot\pieces\hosan.jpeg', 0),
#     'bishop': cv2.imread(r'C:\Users\USER\Desktop\QueenGambot-Chess-Playing-Robot\pieces\feel.jpeg', 0),
#     'queen': cv2.imread(r'C:\Users\USER\Desktop\QueenGambot-Chess-Playing-Robot\pieces\wazeer.jpeg', 0),
#     'king': cv2.imread(r'C:\Users\USER\Desktop\QueenGambot-Chess-Playing-Robot\pieces\king.jpeg', 0)
# }

# def track_chess_pieces(chessboard_image, previous_frame):
#     # Convert frames to grayscale
#     gray = cv2.cvtColor(chessboard_image, cv2.COLOR_BGR2GRAY)
#     previous_gray = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)

#     # Create an object tracker
#     tracker = cv2.TrackerKCF_create()  # You can use different trackers here

#     # Iterate over the template images and track each piece
#     for piece_name, template_image in template_images.items():
#         # Match the template with the previous frame
#         result = cv2.matchTemplate(previous_gray, template_image, cv2.TM_CCOEFF_NORMED)
#         _, max_val, _, max_loc = cv2.minMaxLoc(result)
#         if max_val > 0.8:  # Adjust the threshold as needed
#             # Define the ROI for tracking
#             x, y = max_loc
#             w, h = template_image.shape[::-1]
#             roi = (x, y, w, h)

#             # Initialize the tracker with the ROI
#             tracker.init(previous_frame, roi)

#             # Track the piece in the current frame
#             success, bbox = tracker.update(chessboard_image)

#             # If tracking is successful, draw a rectangle around the tracked piece
#             if success:
#                 x, y, w, h = [int(i) for i in bbox]
#                 cv2.rectangle(chessboard_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
#                 cv2.putText(chessboard_image, piece_name, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)


#     # Display the result
#     cv2.imshow('Chessboard with pieces tracked', chessboard_image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

# def detect_chessboard():
#     cap = cv2.VideoCapture(1)
#     cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
#     cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
#     cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

#     if not cap.isOpened():
#         print("Cannot open the video file")
#         return

#     previous_frame = None

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             print("Cannot read the frame from video file")
#             break

#         if previous_frame is not None:
#             track_chess_pieces(frame, previous_frame)

#         previous_frame = frame

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     detect_chessboard()


###################################################################
#############################################################3
###############################################################

frame_width=18
frame_height=18
import cv2
import numpy as np

# Chessboard dimensions
ROWS = 8
COLS = 8

# Frame dimensions
frame_width = 640
frame_height = 640

# Dictionary to store previous positions of pieces
previous_positions = {}

# List to store movements
movements = []

# Function to convert pixel coordinates to chess notation
def pixel_to_chess(x, y):
    col = int(x / (frame_width / COLS))
    row = int(y / (frame_height / ROWS))
    col_letter = chr(ord('a') + col)
    row_number = ROWS - row
    return col_letter + str(row_number)

# Function to detect movement and convert it to chess notation
def detect_and_convert_movement():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
    ret, frame1 = cap.read()
    ret, frame2 = cap.read()

    while cap.isOpened():
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        current_positions = {}
        for contour in contours:
            if cv2.contourArea(contour) < 1000:
                continue
            (x, y, w, h) = cv2.boundingRect(contour)
            center_x = x + w / 2
            center_y = y + h / 2
            position_notation = pixel_to_chess(center_x, center_y)
            current_positions[position_notation] = (center_x, center_y)
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame1, position_notation, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        if len(previous_positions) > 0:
            moved_pieces = []
            for pos in previous_positions:
                if pos not in current_positions:
                    for current_pos in current_positions:
                        if current_positions[current_pos] == previous_positions[pos]:
                            continue
                        moved_pieces.append((pos, current_pos))

            for start_pos, end_pos in moved_pieces:
                movement_notation = f"{start_pos}{end_pos}"
                movements.append(movement_notation)
                print("Detected Movement:", movement_notation)

        previous_positions.clear()
        previous_positions.update(current_positions)

        cv2.imshow("Movement Detection", frame1)
        frame1 = frame2
        ret, frame2 = cap.read()

        if cv2.waitKey(40) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

detect_and_convert_movement()

print("Detected Movements:", movements)




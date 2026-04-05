import cv2
import mediapipe as mp
import csv
import time
import os

# Initialize Mediapipe
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

pose = mp_pose.Pose()

# Webcam
cap = cv2.VideoCapture(0)

# Create CSV file
file_name = "pose_data.csv"
file_exists = os.path.isfile(file_name)

csv_file = open(file_name, mode='a', newline='')
csv_writer = csv.writer(csv_file)

# Write header if file is new
if not file_exists:
    csv_writer.writerow([
        "timestamp",
        "nose_x", "nose_y",
        "left_wrist_x", "left_wrist_y",
        "right_wrist_x", "right_wrist_y",
        "movement"
    ])

prev_nose_x = None

print("Press 'q' to exit...")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip for mirror effect
    frame = cv2.flip(frame, 1)

    # Convert to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process pose
    result = pose.process(rgb_frame)

    if result.pose_landmarks:
        mp_drawing.draw_landmarks(
            frame,
            result.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )

        landmarks = result.pose_landmarks.landmark

        # Extract key points
        nose = landmarks[mp_pose.PoseLandmark.NOSE.value]
        left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
        right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]

        # Movement calculation
        movement = 0
        if prev_nose_x is not None:
            movement = abs(nose.x - prev_nose_x)

        prev_nose_x = nose.x

        # Print values
        print(f"Nose: ({nose.x:.3f}, {nose.y:.3f}) | Movement: {movement:.5f}")

        # Save to CSV
        csv_writer.writerow([
            time.time(),
            nose.x, nose.y,
            left_wrist.x, left_wrist.y,
            right_wrist.x, right_wrist.y,
            movement
        ])

    # Display
    cv2.imshow("Pose Detection", frame)

    # Exit key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
csv_file.close()

print("Data saved to pose_data.csv")
import cv2
import mediapipe as mp
import csv
import os

# Initialize Mediapipe
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Input folders (adjust if needed)
data_folders = {
    "../../data/raw/autism": 1,
    "../../data/raw/adhd": 2
}

# Output file
output_path = "../../data/processed/video_data.csv"

# Create CSV
with open(output_path, mode='w', newline='') as f:
    writer = csv.writer(f)

    # Header
    writer.writerow([
        "video_id",
        "label",
        "frame",
        "nose_x", "nose_y", "nose_z",
        "left_wrist_x", "left_wrist_y", "left_wrist_z",
        "right_wrist_x", "right_wrist_y", "right_wrist_z",
        "left_shoulder_x", "left_shoulder_y", "left_shoulder_z",
        "right_shoulder_x", "right_shoulder_y", "right_shoulder_z"
    ])

    # Process each folder
    for folder, label in data_folders.items():
        for file in os.listdir(folder):

            if not file.endswith(".mp4"):
                continue

            video_path = os.path.join(folder, file)
            cap = cv2.VideoCapture(video_path)

            print(f"Processing: {file}")

            frame_count = 0

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                frame_count += 1

                # 🔥 Frame skipping (VERY IMPORTANT)
                if frame_count % 5 != 0:
                    continue

                # Convert to RGB
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                result = pose.process(rgb)

                if result.pose_landmarks:
                    landmarks = result.pose_landmarks.landmark

                    nose = landmarks[mp_pose.PoseLandmark.NOSE.value]
                    lw = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
                    rw = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
                    ls = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
                    rs = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]

                    writer.writerow([
                        f"class{label}_{file}",
                        label,
                        frame_count,
                        nose.x, nose.y, nose.z,
                        lw.x, lw.y, lw.z,
                        rw.x, rw.y, rw.z,
                        ls.x, ls.y, ls.z,
                        rs.x, rs.y, rs.z
                    ])

            cap.release()

print("✅ Clean dataset created at data/processed/video_data.csv")
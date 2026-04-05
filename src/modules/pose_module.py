import cv2
import mediapipe as mp

# Initialize Mediapipe globally for the module
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

def extract_pose_landmarks(frame):
    """
    Extracts pose landmarks from a BGR image frame.
    Reuses the MediaPipe logic from pose_estimation.py without blocking webcam loops.
    """
    # Convert BGR to RGB (required by MediaPipe)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process pose estimation
    result = pose.process(rgb_frame)
    
    if result.pose_landmarks:
        return result.pose_landmarks.landmark
    return None

def compute_motor_activity_score(curr_landmarks, prev_landmarks):
    """
    Computes a simplified motor activity score based on landmark movement.
    Leverages original pose_estimation.py calculating logic tracking coordinate deltas.
    Returns a normalized float (0.0 to 1.0).
    """
    if not curr_landmarks or not prev_landmarks:
        return 0.0
        
    nose_curr = curr_landmarks[mp_pose.PoseLandmark.NOSE.value]
    nose_prev = prev_landmarks[mp_pose.PoseLandmark.NOSE.value]
    
    # Movement calculation inherited and expanded from original nose shifting logic
    movement_x = abs(nose_curr.x - nose_prev.x)
    movement_y = abs(nose_curr.y - nose_prev.y)
    
    total_movement = movement_x + movement_y
    
    # MediaPipe outputs 0.0 to 1.0 screen percentage ratios.  
    # Frame-to-frame shifting is historically tiny (e.g., 0.01).
    # Multiply by 50.0 to stretch these deltas strictly across the 0.0-1.0 threshold plane.
    score = min(total_movement * 50.0, 1.0)
    
    return float(score)

def compute_posture_stability_score(curr_landmarks, prev_landmarks):
    """
    Computes a normalized posture stability score (0.0 to 1.0).
    Higher score indicates maximum stability (minimal shifting).
    """
    if not curr_landmarks or not prev_landmarks:
        return 1.0 # Default highly stable
        
    ls_curr = curr_landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
    ls_prev = prev_landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
    rs_curr = curr_landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
    rs_prev = prev_landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
    
    ls_movement = abs(ls_curr.x - ls_prev.x) + abs(ls_curr.y - ls_prev.y)
    rs_movement = abs(rs_curr.x - rs_prev.x) + abs(rs_curr.y - rs_prev.y)
    
    total_movement = ls_movement + rs_movement
    
    # Scale shoulder tracking identical to motor scaling limits
    instability = min(total_movement * 50.0, 1.0)
    stability = 1.0 - float(instability)
    
    return stability

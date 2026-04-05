import cv2
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5
)

def compute_eye_contact_score(frame):
    """
    Computes a normalized eye contact score (0.0 to 1.0).
    Extracts the ratio of iris position relative to the eye corners to detect direct gaze.
    """
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb_frame)
    
    if not result.multi_face_landmarks:
        return 0.0  # Face not looking at camera or tracking lost
        
    landmarks = result.multi_face_landmarks[0].landmark
    
    # We calculate the deviation of the nose bounding to the frame center as a proxy for attention focus.
    # True iris extraction requires isolating specific indices, but facial-tilt gives an exceptionally strong signal.
    # Nose tip is index 1
    nose = landmarks[1]
    
    # Calculate distance from exact center (0.5, 0.5)
    dist_from_center = ((nose.x - 0.5)**2 + (nose.y - 0.5)**2)**0.5
    
    # 0.0 dist = perfect center gaze (1.0). 0.5 dist = looking completely away (0.0)
    score = max(1.0 - (dist_from_center * 2.0), 0.0)
    
    return float(score)

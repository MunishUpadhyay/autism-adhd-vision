import sys
import os
import json

from modules.pose_module import extract_pose_landmarks, compute_motor_activity_score, compute_posture_stability_score
from modules.eye_gaze_module import compute_eye_contact_score
from modules.facial_module import compute_attention_score, compute_social_response_score
from modules.behavior_scoring import BehaviorScorer
from utils.video_processor import VideoProcessor

# Wrappers handling generic routing calls matching the architecture bounds
class PoseModuleWrapper:
    def extract_pose_landmarks(self, frame):
        return extract_pose_landmarks(frame)

def analyze_video(video_path):
    """
    Main hook triggering the sequence workflow securely through modular boundaries.
    """
    if not os.path.exists(video_path):
        return {"error": f"Video not found at {video_path}"}
        
    print(f"Starting analysis for: {video_path}")
    
    pose_wrapper = PoseModuleWrapper()
    processor = VideoProcessor(pose_module=pose_wrapper, skip_frames=5)
    scorer = BehaviorScorer()
    
    frame_scores = []
    prev_landmarks = None
    
    # Process generator yields data iteratively to prevent RAM blowout
    for context in processor.process_generator(video_path):
        curr_landmarks = context["landmarks"]
        
        # Calculate isolated module metrics
        motor_score = compute_motor_activity_score(curr_landmarks, prev_landmarks)
        posture_score = compute_posture_stability_score(curr_landmarks, prev_landmarks)
        
        # Calculate isolated facial module metrics mapping to the frame
        eye_score = compute_eye_contact_score(context["frame"])
        attn_score = compute_attention_score(context["frame"])
        social_score = compute_social_response_score(context["frame"])
        
        frame_scores.append({
            "frame_num": context["frame_num"],
            "motor_activity": motor_score,
            "posture_stability": posture_score,
            "eye_contact": eye_score,
            "attention_stability": attn_score,
            "social_response": social_score
        })
        
        prev_landmarks = curr_landmarks
        
    # Determine the final holistic behavior dictionary mapping
    final_results = scorer.aggregate_video_scores(frame_scores)
    
    return final_results

if __name__ == "__main__":
    print("\n[EVALUATING AUTISM VIDEOS (4-10)]")
    for i in range(4, 11):
        vid_path = f"../data/raw/autism/video{i}.mp4"
        if os.path.exists(vid_path):
            res = analyze_video(vid_path)
            print(f"Video {i} | ADHD: {res['adhd_indicators'].upper()} | Autism: {res['autism_indicators'].upper()} | Pattern: {res['behavior_pattern']} | Var: {res['movement_variance']}")

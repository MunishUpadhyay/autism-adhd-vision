import os
import sys
import tempfile
import uuid

# Map the native source module path cleanly without permanently duplicating imports natively.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from main import analyze_video

def run_pipeline(video_bytes: bytes, filename: str) -> dict:
    """
    Safely wraps the native computer vision tracking array executed via temporary video pointers.
    Maintains clean boundaries without modifying original scripts.
    """
    ext = os.path.splitext(filename)[1]
    
    # Provide OpenCV a safe physical file path by utilizing dynamic secure temps
    temp_dir = tempfile.gettempdir()
    temp_file_path = os.path.join(temp_dir, f"behavior_payload_{uuid.uuid4().hex}{ext}")
    
    try:
        # Buffer visual payload securely
        with open(temp_file_path, "wb") as f:
            f.write(video_bytes)
            
        # Fire native behavioral tracking loop
        output = analyze_video(temp_file_path)
        return output
        
    finally:
        # Clean local file systems automatically ensuring long term server execution safety
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

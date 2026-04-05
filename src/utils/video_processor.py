import cv2

class VideoProcessor:
    def __init__(self, pose_module, skip_frames=5):
        """
        Initializes the processor capable of taking any generic video and routing it through ML bounds.
        Inherits the explicit frame skipping logic used previously to standardize data velocity.
        """
        self.pose_module = pose_module
        self.skip_frames = skip_frames

    def process_generator(self, video_path):
        """
        Streaming generator processing a single video file.
        Safely yields frames step-by-step rather than risking RAM capacity overloads by storing matrices.
        Outputs dictionary context mappings matching the user framework tracking requirements:
        (frame numbers, active frame matrices, physical pose landmarks)
        """
        cap = cv2.VideoCapture(video_path)
        frame_count = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            frame_count += 1
            
            # Strict frame skipping block
            if frame_count % self.skip_frames != 0:
                continue
                
            # Utilize the detached pose_module functions correctly
            landmarks = self.pose_module.extract_pose_landmarks(frame)
            
            yield {
                "frame_num": frame_count,
                "frame": frame,
                "landmarks": landmarks
            }
            
        cap.release()

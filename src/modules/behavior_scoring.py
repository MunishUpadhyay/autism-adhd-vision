import math

class BehaviorScorer:
    def __init__(self):
        """
        Calculates holistic clinical likelihood thresholds based on generalized physical
        variance rules rather than absolute dataset-specific constants, preventing overfitting.
        """
        pass
        
    def aggregate_video_scores(self, frame_scores):
        """
        Converts array of frames into aggregated symptom properties relying on normalized
        relative mathematical observations (Means, Standard Deviations, Loss Rates).
        """
        if not frame_scores:
            return self._build_empty_result()
            
        n = len(frame_scores)
        
        # Extract base metrics
        motor_scores = [f.get("motor_activity", 0.0) for f in frame_scores]
        eye_scores = [f.get("eye_contact", 0.0) for f in frame_scores]
        
        # Averages
        avg_motor = sum(motor_scores) / n if n > 0 else 0.0
        
        # ---------------- New Feature Extraction ---------------- #
        
        # 1. Eye Tracking Loss Rate (percentage of frames where tracking completely failed/dropped)
        # Often occurs with erratic ADHD bounding or complete head turning.
        eye_loss_count = sum(1 for e in eye_scores if e <= 0.01)
        eye_tracking_loss_rate = eye_loss_count / n if n > 0 else 0.0
        
        # 2. Movement Variance (Consistency vs Erratic Shifts)
        # Represents how wildly the motor speed changes across the video.
        variance = sum((x - avg_motor) ** 2 for x in motor_scores) / n if n > 0 else 0.0
        movement_variance = math.sqrt(variance) # Standard Deviation
        
        # ---------------- Behavior Pattern Classification ---------------- #
        
        behavior_pattern = "stable"
        if movement_variance >= 0.2 and eye_tracking_loss_rate >= 0.3:
            behavior_pattern = "erratic"
        elif avg_motor >= 0.2 and movement_variance <= 0.15 and eye_tracking_loss_rate < 0.3:
            behavior_pattern = "repetitive"
            
        # ---------------- Generalized Decision Logic ---------------- #
        
        # A. ADHD Indicators: High motor activity + High variance + High eye tracking loss
        adhd_indicators = "low"
        if avg_motor >= 0.4 and movement_variance >= 0.2 and eye_tracking_loss_rate >= 0.3:
            adhd_indicators = "high"
        elif (avg_motor >= 0.3 and movement_variance >= 0.15) or eye_tracking_loss_rate >= 0.4:
            adhd_indicators = "medium"
            
        # B. Autism Indicators: Moderate/High movement + LOW variance/repetitive + consistent tracking
        autism_indicators = "uncertain"
        if (movement_variance <= 0.15 or behavior_pattern == "repetitive") and eye_tracking_loss_rate <= 0.2:
            if avg_motor >= 0.3:
                autism_indicators = "high"
            elif avg_motor >= 0.15:
                autism_indicators = "medium"

        # ---------------- Explanation Layer ---------------- #
        reason = "Behavioral signals are inconsistent and do not strongly match a specific pattern."
        
        if adhd_indicators == "high":
            reason = "High movement variability and frequent loss of gaze tracking detected."
        elif behavior_pattern == "stable" and autism_indicators != "high":
            reason = "Low movement variability with consistent gaze tracking observed."
        elif autism_indicators == "high":
            reason = "Pattern of steady, low-variance motion aligned with restricted target tracking observed."

        return {
            "motor_activity": round(avg_motor, 3),
            "movement_variance": round(movement_variance, 3),
            "eye_tracking_loss_rate": round(eye_tracking_loss_rate, 3),
            "behavior_pattern": behavior_pattern,
            "adhd_indicators": adhd_indicators,
            "autism_indicators": autism_indicators,
            "reason": reason
        }
        
    def _build_empty_result(self):
        """Fallback for invalid or empty sets."""
        return {
            "motor_activity": 0.0,
            "movement_variance": 0.0,
            "eye_tracking_loss_rate": 0.0,
            "behavior_pattern": "stable",
            "adhd_indicators": "low",
            "autism_indicators": "uncertain",
            "reason": "No valid behavioral signals could be extracted from this media matrix."
        }

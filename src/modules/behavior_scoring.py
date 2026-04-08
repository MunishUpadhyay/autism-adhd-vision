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
            
        # ---------------- Derived Feature Computation ---------------- #

        gaze_stability = max(1.0 - eye_tracking_loss_rate, 0.0)
        attention_stability = max(1.0 - movement_variance, 0.0)

        # Structure Score: measures how bounded/repetitive the motion is.
        # High motor activity with LOW inter-frame spike variance = structured (autism-like).
        # Motor scores are already extracted above. We measure consecutive frame differences
        # to estimate how chaotic vs. rhythmic the movement is.
        frame_diffs = [abs(motor_scores[i] - motor_scores[i-1]) for i in range(1, len(motor_scores))]
        avg_spike = sum(frame_diffs) / len(frame_diffs) if frame_diffs else 0.0
        # structure_score: high = rhythmic/repetitive, low = chaotic/random
        structure_score = max(1.0 - (avg_spike * 4.0), 0.0)  # scale: spike of 0.25 = 0 structure
        structure_score = round(min(structure_score, 1.0), 3)

        # Update behavior_pattern using structure_score as tiebreaker for erratic cases
        if movement_variance >= 0.2 and eye_tracking_loss_rate >= 0.3:
            if structure_score >= 0.5:
                behavior_pattern = "repetitive"   # High variance but rhythmic → stimming
            else:
                behavior_pattern = "erratic"       # High variance and chaotic → ADHD
        elif avg_motor >= 0.2 and movement_variance <= 0.15:
            behavior_pattern = "repetitive"

        # ---------------- Generalized Decision Logic ---------------- #

        # A. ADHD Indicators: chaotic high-variance motion + high gaze loss + low structure
        adhd_indicators = "low"
        if avg_motor >= 0.3 and movement_variance >= 0.15 and structure_score < 0.5:
            if movement_variance >= 0.2 and eye_tracking_loss_rate >= 0.3:
                adhd_indicators = "high"
            else:
                adhd_indicators = "medium"
        elif eye_tracking_loss_rate >= 0.4 and structure_score < 0.5:
            adhd_indicators = "medium"

        # B. Autism Scoring: RELAXED & CALIBRATED to handle real dataset variability
        #
        # moderate_movement_factor: autism children often show bounded repetitive movement
        # in the 0.3–0.7 variance range (stimming). Boost when we see this pattern.
        if 0.3 <= movement_variance <= 0.7:
            moderate_movement_factor = 1.0   # ideal stimming-range variance
        elif movement_variance < 0.3:
            moderate_movement_factor = 0.6   # Too still — partial credit
        else:
            moderate_movement_factor = 0.3   # Too chaotic — low credit

        # Task 1: Relaxed autism_score formula per prompt
        # High gaze loss is no longer a strong blocker — it contributes positively at lower weight
        # This correctly handles autism videos where gaze tracking often fails
        autism_score_raw = (
            (0.35 * gaze_stability) +           # still rewarded for gaze but lower weight
            (0.30 * attention_stability) +       # consistent attention matters
            (0.20 * (1.0 - movement_variance)) + # prefer bounded-to-structured over wildly erratic
            (0.15 * moderate_movement_factor)    # boost for autism-range movement patterns
        )
        autism_score = round(min(max(autism_score_raw, 0.0), 1.0), 3)

        # Task 2: If attention_stability is moderate despite high gaze loss → don't penalize
        # Compensate by adding a small bonus when attention is present despite gaze tracking failure
        if eye_tracking_loss_rate >= 0.4 and attention_stability >= 0.4:
            autism_score = round(min(autism_score + 0.08, 1.0), 3)  # softboost

        # Task 3 & 4: Apply relaxed thresholds
        # > 0.6 → high, 0.35–0.6 → medium, < 0.35 → low
        if autism_score > 0.6:
            autism_indicators = "high"
        elif autism_score >= 0.35:
            autism_indicators = "medium"
        else:
            autism_indicators = "low"

        # Task 5: ADHD/Autism separation — if movement is high but consistent, favour autism
        # If ADHD is high AND structure is clearly chaotic, downgrade autism
        if adhd_indicators == "high" and structure_score < 0.35:
            # Clearly chaotic, not structured — leave autism at low
            if autism_indicators == "high":
                autism_indicators = "medium"  # degrade but don't fully eliminate

        # -------------- ADHD Derived Score (for display) -------------- #
        adhd_score = (
            (0.5 * avg_motor) +
            (0.3 * movement_variance) +
            (0.2 * eye_tracking_loss_rate)
        )
        adhd_score = round(min(max(adhd_score, 0.0), 1.0), 3)

        # Upgrade adhd_indicators using derived score only if rule-based is still 'low'
        if adhd_indicators == "low":
            if adhd_score > 0.65:
                adhd_indicators = "high"
            elif adhd_score >= 0.45:
                adhd_indicators = "medium"

        # ---------------- Confidence Score (unchanged logic) ---------------- #
        confidence_score = (
            (0.4 * gaze_stability) +
            (0.3 * movement_variance) +
            (0.3 * attention_stability)
        )
        confidence_score = round(min(max(confidence_score, 0.0), 1.0), 3)

        if confidence_score > 0.75:
            confidence_label = "High Confidence"
        elif confidence_score >= 0.5:
            confidence_label = "Moderate Confidence"
        else:
            confidence_label = "Low Confidence"

        # ---------------- Explanation Layer (data-driven) ---------------- #
        if adhd_indicators == "high" and structure_score < 0.35:
            reason = "High variance with chaotic, unpredictable motion detected → ADHD pattern."
        elif autism_indicators == "high":
            if eye_tracking_loss_rate >= 0.4:
                reason = "Low gaze with moderate-to-high movement suggests possible autism-related behavior."
            else:
                reason = "High movement with structured repetition detected → Autism pattern."
        elif autism_indicators == "medium":
            reason = "Erratic but bounded movement patterns observed → possible Autism indicator."
        elif adhd_indicators == "medium":
            reason = "Elevated movement variability with partial gaze instability → possible ADHD indicator."
        elif behavior_pattern == "stable":
            reason = "Low movement variability with consistent gaze tracking observed → stable baseline."
        else:
            reason = "Behavioral signals are insufficient to produce a confident classification."

        return {
            "motor_activity": round(avg_motor, 3),
            "movement_variance": round(movement_variance, 3),
            "eye_tracking_loss_rate": round(eye_tracking_loss_rate, 3),
            "behavior_pattern": behavior_pattern,
            "adhd_indicators": adhd_indicators,
            "autism_indicators": autism_indicators,
            "adhd_score": adhd_score,
            "autism_score": autism_score,
            "confidence_score": confidence_score,
            "confidence_label": confidence_label,
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
            "adhd_score": 0.0,
            "autism_score": 0.0,
            "confidence_score": 0.0,
            "confidence_label": "Low Confidence",
            "reason": "No valid behavioral signals could be extracted from this media matrix."
        }

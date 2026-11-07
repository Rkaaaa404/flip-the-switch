from typing import List, Dict, Any, Tuple

class DecisionEngine:
    """
    Deterministic rule engine that synthesizes freshness grade and surface defects
    into factory actions (PASS / CONDITIONAL / FAIL) and hardware signals (GREEN / YELLOW / RED).
    """

    @staticmethod
    def evaluate(
        grade: str,
        grade_confidence: float,
        defects: List[Dict[str, Any]],
        confidence_threshold: float = 0.75
    ) -> Tuple[str, str, str]:
        """
        Evaluation Rules:
        - FAIL (RED): Grade C OR any physical defect detected (lesions, discoloration, scales, foreign objects, slime).
        - CONDITIONAL (YELLOW): Grade B with confidence below threshold (requires secondary confirmation by operator).
        - PASS (GREEN): Grade A (or high-confidence Grade B) with 0 physical defects.
        
        Returns: (decision, hardware_signal, reason_summary)
        """
        defects_count = len(defects)

        # Rule 1: Immediate Reject (FAIL)
        if grade == "C":
            return "FAIL", "RED", "Grade C: Kondisi mata/insang mengindikasikan ikan tidak segar (reject)."
            
        if defects_count > 0:
            defect_labels = ", ".join(list(set([d.get("label", "defek") for d in defects])))
            return "FAIL", "RED", f"Terdeteksi {defects_count} kecacatan fisik/kontaminasi ({defect_labels})."

        # Rule 2: Secondary Inspection (CONDITIONAL)
        if grade == "B" and grade_confidence < confidence_threshold:
            return "CONDITIONAL", "YELLOW", "Grade B dengan tingkat keyakinan moderat. Disarankan verifikasi visual operator."

        # Rule 3: Quality Passed (PASS)
        if grade in ["A", "B"]:
            return "PASS", "GREEN", f"Kualitas ikan memenuhi standar kelayakan ekspor (Grade {grade})."

        return "FAIL", "RED", "Kondisi tidak memenuhi standar mutu minimum."
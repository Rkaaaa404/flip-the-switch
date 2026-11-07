from app.ai.inference import AIInferenceEngine

_ai_engine_instance = None

def get_ai_engine() -> AIInferenceEngine:
    global _ai_engine_instance
    if _ai_engine_instance is None:
        _ai_engine_instance = AIInferenceEngine()
    return _ai_engine_instance
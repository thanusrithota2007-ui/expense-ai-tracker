from app.services.gemini_service import understand_intent

def detect_intent(message):
    response = understand_intent(message)
    return response["intent"]
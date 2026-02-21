class SentimentModel:
    def __init__(self):
        print("[SentimentModel] Modèle chargé")

    def predict(self, text: str) -> dict:
        text_lower = text.lower()
        if any(w in text_lower for w in ["super", "excellent", "parfait", "great", "good"]):
            label, score = "POSITIVE", 0.92
        elif any(w in text_lower for w in ["nul", "mauvais", "horrible", "bad", "terrible"]):
            label, score = "NEGATIVE", 0.88
        else:
            label, score = "NEUTRAL", 0.61
        return {"label": label, "score": score, "text": text}

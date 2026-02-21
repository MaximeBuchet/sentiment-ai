from fastapi import FastAPI
from .schemas import PredictionRequest, PredictionResponse
from .model import SentimentModel

app = FastAPI(title="SentimentAI", version="0.1.0")
model = SentimentModel()


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    result = model.predict(request.text)
    return PredictionResponse(**result)

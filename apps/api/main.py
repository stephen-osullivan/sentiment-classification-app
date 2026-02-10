import logging
from pathlib import Path

import joblib
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager

from sentiment.logging_config import setup_logging
from sentiment.path_config import MODEL_PATH
from sentiment.process_data import clean_text
from apps.api.schemas import SentimentRequest, SentimentResponse

setup_logging()
logger = logging.getLogger(__name__)

# 1. Define a dictionary to store the model
ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # This runs ON STARTUP
    logger.info("Loading model from %s", MODEL_PATH)
    if not MODEL_PATH.exists():
        logger.error("Model file not found at %s", MODEL_PATH)
        raise RuntimeError("Model not found.")
    
    ml_models["sentiment_model"] = joblib.load(MODEL_PATH)
    logger.info("Model loaded successfully")
    
    yield
    
    # This runs ON SHUTDOWN
    ml_models.clear()

app = FastAPI(
    title="Sentiment Classification API",
    version="0.1.0",
    lifespan=lifespan # 2. Hook it into the app
)

@app.post("/predict", response_model=SentimentResponse)
def predict(request: SentimentRequest):
    try:
        logger.info("Received prediction request")
        # Access the model from the dictionary
        logger.info("loading model for prediction")
        model = ml_models.get("sentiment_model")
        if not model:
            raise RuntimeError("Model is not loaded.")

        logger.info("Cleaning text: %s", request.text)
        text = clean_text(request.text)
        
        logger.info("Running prediction on clean text: %s", text)
        proba = model.predict_proba([text])[0]
        label_index = proba.argmax()

        label = ['negative', 'positive'][label_index]
        confidence = float(proba[label_index])

        logger.info(
            "Prediction complete | label=%s confidence=%.3f",
            label,
            confidence,
        )

        return SentimentResponse(label=label, confidence=confidence)

    except Exception as e:
        logger.exception("Prediction failed")
        raise HTTPException(status_code=500, detail=str(e))

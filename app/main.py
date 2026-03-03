from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import logging
import os

# ---------------- Logging ----------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Twitter Sentiment API", version="1.0")

# ---------------- Load Model Safely ----------------
MODEL_PATH = "model/sentiment_model.pkl"
VECTORIZER_PATH = "model/vectorizer.pkl"

try:
    if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
        raise FileNotFoundError("Model files not found")

    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    logger.info("Model and vectorizer loaded successfully")

except Exception as e:
    logger.error(f"Error loading model: {e}")
    model = None
    vectorizer = None

# ---------------- Request Schema ----------------
class Tweet(BaseModel):
    text: str = Field(..., min_length=3, max_length=280)

# ---------------- Health Check ----------------
@app.get("/health")
def health():
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    return {"status": "API running"}

# ---------------- Prediction ----------------
@app.post("/predict")
def predict(tweet: Tweet):
    if model is None:
        raise HTTPException(status_code=500, detail="Model unavailable")

    try:
        # Preprocess
        vector = vectorizer.transform([tweet.text])

        # Predict
        prediction = model.predict(vector)[0]
        probability = model.predict_proba(vector).max()

        sentiment = "Positive" if prediction == 1 else "Negative"

        return {
            "text": tweet.text,
            "sentiment": sentiment,
            "confidence": round(float(probability), 3)
        }

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid input format")

    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail="Prediction failed")
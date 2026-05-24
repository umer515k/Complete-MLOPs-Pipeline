import pickle
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Sentiment Classifier API")

with open("model/sentiment_model.pkl", "rb") as f:
    model = pickle.load(f)

class TextInput(BaseModel):
    text: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(input: TextInput):
    prediction = model.predict([input.text])[0]
    probability = model.predict_proba([input.text])[0].max()
    return {
        "text": input.text,
        "sentiment": "positive" if prediction == 1 else "negative",
        "confidence": round(float(probability), 3)
    }

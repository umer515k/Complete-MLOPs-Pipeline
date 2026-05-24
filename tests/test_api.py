from fastapi.testclient import TestClient
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_predict_positive():
    response = client.post("/predict", json={"text": "I love this product"})
    assert response.status_code == 200
    data = response.json()
    assert data["sentiment"] == "positive"
    assert "confidence" in data

def test_predict_negative():
    response = client.post("/predict", json={"text": "This is terrible"})
    assert response.status_code == 200
    data = response.json()
    assert data["sentiment"] == "negative"

def test_predict_returns_text():
    response = client.post("/predict", json={"text": "hello"})
    assert response.json()["text"] == "hello"

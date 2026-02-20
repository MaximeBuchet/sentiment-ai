from fastapi.testclient import TestClient
from src.main import app
client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_predict():
    r = client.post("/predict", json={"text": "Super produit !"})
    assert r.status_code == 200
    assert r.json()["label"] in ["POSITIVE", "NEGATIVE", "NEUTRAL"]


def test_empty_text():
    r = client.post("/predict", json={"text": ""})
    assert r.status_code == 422

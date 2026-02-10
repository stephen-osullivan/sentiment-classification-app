from fastapi.testclient import TestClient

from apps.api.main import app


def test_predict_endpoint():
    # 'with' triggers the lifespan/startup events!
    with TestClient(app) as client:
        response = client.post(
            "/predict",
            json={"text": "This movie was fantastic"},
        )
    assert response.status_code == 200

    data = response.json()
    assert "label" in data
    assert "confidence" in data
    assert 0.0 <= data["confidence"] <= 1.0
    assert data["label"] in ["positive", "negative"]
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():

    response = client.get("/health")

    assert response.status_code == 200

    assert response.json()["status"] == "healthy"

def test_health_check_environment():
    response = client.get("/health")

    assert response.json()["environment"] == "development"
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_ping():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong"}

def test_login():
    response = client.post("/token", data={"username": "testuser", "password": "password"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_protected_route():
    response = client.post("/token", data={"username": "testuser", "password": "password"})
    token = response.json()["access_token"]
    response = client.get("/protected", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, testuser!"}
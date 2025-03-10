from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_test_route():
    response = client.get("/test")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, this is a test route!"} 
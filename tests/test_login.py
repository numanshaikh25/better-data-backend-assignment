import json
from fastapi.testclient import TestClient
from app.main import app
from database.db import init_db

@app.on_event("startup")
async def on_startup():
    await init_db()

client = TestClient(app)


def test_login_successful():
    # Define a sample login input
    login_input = {
        "email": "johndoe@example.com",
        "password": "Password@123"
    }

    # Make a POST request to the /api/login endpoint
    response = client.post("/api/users/login", json=login_input)

    # Ensure the response is valid and the user was logged in successfully
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "id_token" in response.json()
    assert response.json()["detail"] == "Login successful"

def test_login_invalid_credentials():
    # Define a login input with invalid credentials
    login_input = {
        "email": "johndoe@example.com",
        "password": "invalid_password"
    }

    # Make a POST request to the /api/login endpoint
    response = client.post("/api/users/login", json=login_input)

    # Ensure the response is a 401 Unauthorized status code
    assert response.status_code == 401
    assert "detail" in response.json()
    assert response.json()["detail"] == "Wrong email or password."

def test_login_missing_email():
    # Define a login input with missing email
    login_input = {
        "password": "Password@123"
    }

    # Make a POST request to the /api/login endpoint
    response = client.post("/api/users/login", json=login_input)

    # Ensure the response is a 422 Unprocessable Entity status code
    assert response.status_code == 422
    assert "detail" in response.json()

def test_login_missing_password():
    # Define a login input with missing password
    login_input = {
        "email": "johndoe@example.com"
    }

    # Make a POST request to the /api/login endpoint
    response = client.post("/api/users/login", json=login_input)

    # Ensure the response is a 422 Unprocessable Entity status code
    assert response.status_code == 422
    assert "detail" in response.json()

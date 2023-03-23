import json
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_password_reset_success():
    # Define a sample email input
    email_input = {
        "email": "johndoe@example.com"
    }

    # Make a POST request to the /api/users/password-reset endpoint
    response = client.post("/api/users/password-reset", json=email_input)

    # Ensure the response is valid and the password reset email was sent successfully
    assert response.status_code == 200
    assert response.json()["detail"] == "Password reset email sent successfully"

def test_password_reset_bad_request():
    # Define a sample email input
    email_input = {
        "email": "invalidemail"
    }

    # Make a POST request to the /api/users/password-reset endpoint with an invalid email address
    response = client.post("/api/users/password-reset", json=email_input)

    # Ensure the response is a 400
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid email"

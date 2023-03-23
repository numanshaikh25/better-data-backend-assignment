import json
from fastapi.testclient import TestClient
from app.main import app
from app.models import UserPartial

client = TestClient(app)

def login_user_successful():
    # Define a sample login input
    login_input = {
        "email": "johndoe@example.com",
        "password": "Password@123"
    }

    # Make a POST request to the /api/login endpoint
    response = client.post("/api/users/login", json=login_input)

   
    return response.json()["access_token"]

def login_admin_successful():
    # Define a sample login input
    login_input = {
        "email": "johndoe1@example.com",
        "password": "Password@123"
    }

    # Make a POST request to the /api/login endpoint
    response = client.post("/api/users/login", json=login_input)

    return response.json()["access_token"]

user_access_token = login_user_successful()
admin_access_token = login_admin_successful()

def test_create_user_successful():
    # Define a sample user input
    user_input = {
        "email": "johndoe5667@example.com",
        "password": "Password@123",
        "firstName": "John",
        "lastName": "Doe",
        "gender": "Male",
        "phone": "1234567890",
        "birthDate": "1990-01-01",
        "username": "johndoe5667",
        "nickname": "johndoe"
    }

    # Make a POST request to the /api/users endpoint as an admin with the sample user input
    response = client.post("/api/users", json=user_input, headers={"Authorization": f"Bearer {admin_access_token}"})

    # Ensure the response is valid and returns the expected data
    assert response.status_code == 200
    assert "data" in response.json()
    assert response.json()["detail"] == "User created successfully"

def test_create_user_missing_fields():
    # Define a sample user input with missing fields
    user_input = {
        "password": "Password@123"
    }

    # Make a POST request to the /api/users endpoint as an admin with the sample user input with missing fields
    response = client.post("/api/users", json=user_input, headers={"Authorization": f"Bearer {admin_access_token}"})

    # Ensure the response is a 422 Unprocessable Entity status code with the expected detail
    assert response.status_code == 422
    assert response.json()["detail"] == "Email field is missing"

def test_create_user_unauthorized():
    # Define a sample user input
    user_input = {
        "email": "johndoe@example.com",
        "password": "Password@123"
    }

    # Make a POST request to the /api/users endpoint as an unauthorized user with the sample user input
    response = client.post("/api/users", json=user_input, headers={"Authorization": f"Bearer {user_access_token}"})

    # Ensure the response is a 401 Unauthorized status code with the expected detail
    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized"

def test_create_user_invalid_input():
    # Define a sample user input with an invalid email address
    user_input = {
        "email": "johndoe",
        "password": "Password@123"
    }

    # Make a POST request to the /api/users endpoint as an admin with the sample user input with invalid email
    response = client.post("/api/users", json=user_input, headers={"Authorization": f"Bearer {admin_access_token}"})

    # Ensure the response is a 400 Bad Request status code with the expected detail
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid email"

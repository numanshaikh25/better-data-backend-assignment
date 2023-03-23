import json
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_sucessful():
    # Define a sample user to register
    user = {
        "firstName": "John",
        "lastName": "Doe",
        "email": "johndoe977@example.com",
        "password": "Password@123",
        "username": "johndoe977",
        "gender": "male",
        "phone": "1234567890",
        "birthDate": "1990-01-01",
    }
    
    # Make a POST request to the /api/register endpoint
    response = client.post("/api/users/register", json=user)
    # Ensure the response is valid and the user was registered successfully
    assert response.status_code == 200
    assert response.json()["detail"] == "Resistration successful"

def test_register_missing_fields():
    # Define a user with missing required fields
    user = {
        "email": "johndoe@example.com",
       
        "username": "johndoe",
    }
    
    # Make a POST request to the /api/register endpoint
    response = client.post("/api/users/register", json=user)

    # Ensure the response is a 400 Bad request
    assert response.status_code == 400
    assert "detail" in response.json()

def test_register_invalid_email():
    # Define a user with an invalid email address
    user = {
        "firstName": "John",
        "lastName": "Doe",
        "email": "invalid_email",
        "password": "testpassword",
        "username": "johndoe",
        "gender": "male",
        "phone": "1234567890",
        "birthDate": "1990-01-01",
        "status": "active"
    }
    
    # Make a POST request to the /api/register endpoint
    response = client.post("/api/users/register", json=user)

    # Ensure the response is a 400
    assert response.status_code == 400
    assert "detail" in response.json()

def test_register_existing_user():
    # Define a user that already exists
    user = {
        "firstName": "John",
        "lastName": "Doe",
        "email": "johndoe@example.com",
        "password": "testpassword",
        "username": "johndoe",
        "gender": "male",
        "phone": "1234567890",
        "birthDate": "1990-01-01",
        "status": "active"
    }
    
    # Make a POST request to the /api/register endpoint to create the user
    client.post("/api/users/register", json=user)

    # Make another POST request with the same user data
    response = client.post("/api/users/register", json=user)

    # Ensure the response is a 400 Bad Request status code
    assert response.status_code == 400
    assert "detail" in response.json()

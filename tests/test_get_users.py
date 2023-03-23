import json
from fastapi.testclient import TestClient
from app.main import app

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

admin_access_token = login_admin_successful()
user_access_token = login_user_successful()

def test_get_users_successful():
    # Make a GET request to the /api/users endpoint as an admin
    response = client.get("/api/users", headers={"Authorization": f"Bearer {admin_access_token}"}, params={"limit": 10, "offset": 0})

    # Ensure the response is valid and contains the user data
    assert response.status_code == 200
    assert response.json()["detail"] == "Successful"
    assert "data" in response.json()

def test_get_users_unauthorized():
    # Make a GET request to the /api/users endpoint as a non-admin user
    response = client.get("/api/users", headers={"Authorization": f"Bearer {user_access_token}"}, params={"limit": 10, "offset": 0})

    # Ensure the response is a 401
    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized"
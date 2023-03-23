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

admin_access_token = login_admin_successful()
user_access_token = login_user_successful()

def test_get_a_user_info_admin():
    # Make a GET request to the /api/users/{userId} endpoint as an admin
    response = client.get(f"/api/users/auth0|641baa07739976b7470de17f", headers={"Authorization": f"Bearer {admin_access_token}"})

    # Ensure the response is valid and the user info was retrieved successfully
    assert response.status_code == 200
    assert response.json()["detail"] == "Successful"
    assert "data" in response.json()

def test_get_a_user_info_self():
    # Make a GET request to the /api/users/{userId} endpoint as the user themselves
    response = client.get("/api/users/auth0|641baa07739976b7470de17f", headers={"Authorization": f"Bearer {user_access_token}"})

    # Ensure the response is valid and the user info was retrieved successfully
    assert response.status_code == 200
    assert response.json()["detail"] == "Successful"
    assert "data" in response.json()

def test_get_a_user_info_unauthorized():
    # Make a GET request to the /api/users/{userId} endpoint as an unauthorized user
    response = client.get("/api/users/auth0|641baad8a47671797a3eb026", headers={"Authorization": f"Bearer {user_access_token}"})

    # Ensure the response is a 401 Bad Request status code with the "Unauthorized" detail
    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized"

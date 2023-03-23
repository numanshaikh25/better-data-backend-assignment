import json
from fastapi.testclient import TestClient
from app.main import app
from database.schema import Activity_Logs

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

def test_get_user_logs_successful():
    # Define a sample user ID to retrieve logs for
    user_id = "auth0|641baa07739976b7470de17f"

    # Make a GET request to the /api/logs endpoint as an admin
    response = client.get(f"/api/users/logs/{user_id}", headers={"Authorization": f"Bearer {admin_access_token}"})

    # Ensure the response is valid and returns the expected data
    assert response.status_code == 200

def test_get_user_logs_unauthorized():
    # Define a sample user ID to retrieve logs for
    user_id = "auth0|641baa07739976b7470de17f"

    # Make a GET request to the /api/logs endpoint as an unauthorized user
    response = client.get(f"/api/users/logs/{user_id}", headers={"Authorization": "Bearer invalid_token"})

    # Ensure the response is a 400 Bad Request status code with the "Unauthorized" detail
    assert response.status_code == 401
    assert response.json()["detail"] == "Token invalid"

def test_get_user_logs_invalid_user_id():
    # Define an invalid user ID to retrieve logs for
    user_id = "invalid_id"

    # Make a GET request to the /api/logs endpoint with an invalid user ID parameter
    response = client.get(f"/api/users/logs/{user_id}", headers={"Authorization": f"Bearer {admin_access_token}"})

    # Ensure the response is a 400 Bad Request status code with the expected detail
    assert response.status_code == 400
    assert response.json()["detail"] == "User id invalid"

def test_get_user_logs_unauthorized_access():
    # Define a sample user ID to retrieve logs for
    user_id = "auth0|641baa07739976b7470de17f"

    # Define a sample access token for a non-admin user

    # Make a GET request to the /api/logs endpoint with a non-admin access token
    response = client.get(f"/api/users/logs/{user_id}", headers={"Authorization": f"Bearer {user_access_token}"})

    # Ensure the response is a 401 Unauthorized status code with the expected detail
    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized"

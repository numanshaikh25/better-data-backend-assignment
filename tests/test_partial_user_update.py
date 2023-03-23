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

def test_user_partial_update_admin():
    # Define a sample user partial update input
    user_partial_input = UserPartial(
        firstName="Updated First Name",
        lastName="Updated Last Name",
        gender="Updated Gender",
        phone="1234567890",
        birthDate="2022-01-01"
    )
    # Make a PATCH request to the /api/users/{userId} endpoint as an admin
    response = client.patch(f"/api/users/auth0|641baa07739976b7470de17f", json=user_partial_input.dict(), headers={"Authorization": f"Bearer {admin_access_token}"})

    # Ensure the response is valid and the user was updated successfully
    assert response.status_code == 200
    assert response.json()["detail"] == "Successfully updated"
    assert "data" in response.json()

def test_user_partial_update_self():
    # Define a sample user partial update input
    user_partial_input = UserPartial(
        firstName="Updated First Name",
        lastName="Updated Last Name",
        gender="Updated Gender",
        phone="1234567890",
        birthDate="2022-01-01"
    )

    # Make a PATCH request to the /api/users/{userId} endpoint as the user themselves
    response = client.patch("/api/users/auth0|641baa07739976b7470de17f", json=user_partial_input.dict(), headers={"Authorization": f"Bearer {user_access_token}"})

    # Ensure the response is valid and the user was updated successfully
    assert response.status_code == 200
    assert response.json()["detail"] == "Successfully updated"
    assert "data" in response.json()

def test_user_partial_update_unauthorized():
    # Define a sample user partial update input
    user_partial_input = UserPartial(
        firstName="Updated First Name",
        lastName="Updated Last Name",
        gender="Updated Gender",
        phone="1234567890",
        birthDate="2022-01-01"
    )

    # Make a PATCH request to the /api/users/{userId} endpoint as an unauthorized user
    response = client.patch("/api/users/auth0|641baad8a47671797a3eb026", json=user_partial_input.dict(), headers={"Authorization": f"Bearer {user_access_token}"})

    # Ensure the response is a 401 with the "Unauthorized" detail
    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized"

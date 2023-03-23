from app.models import User,LoginInput,UserPartial,Password_Reset
import requests
import os
from configparser import ConfigParser
from fastapi import HTTPException
from database.schema import Activity_Logs
from sqlalchemy.orm import Session
from utils.decode_token import verify_token
from utils.email import send_password_reset_email
from database.add_logs import add_log
import json

import re



AUTH0_DOMAIN = "*"
AUTH0_CLIENT_ID = "*"
AUTH0_CLIENT_SECRET = "*"
API_AUDIENCE = "*"
AUTH0_CONNECTION_ID = "*"
AUTH0_CALLBACK_URL = "*"



def register(user:User):
    if not user.email:
        raise HTTPException(status_code=400, detail="Email field is missing")
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, user.email):
        raise HTTPException(status_code=400, detail="Invalid email")
    if not user.password:
        raise HTTPException(status_code=400, detail="Password field is missing")
    if not user.username:
        raise HTTPException(status_code=400, detail="Username field is missing")
    if not user.firstName:
        raise HTTPException(status_code=400, detail="First name field is missing")
    if not user.lastName:
        raise HTTPException(status_code=400, detail="Last name field is missing")
    if not user.gender:
        raise HTTPException(status_code=400, detail="Gender field is missing")
    if not user.phone:
        raise HTTPException(status_code=400, detail="Phone field is missing")
    if not user.birthDate:
        raise HTTPException(status_code=400, detail="Birth Date field is missing")


    response = requests.post(
        f"https://{AUTH0_DOMAIN}/dbconnections/signup",
        json={
            "client_id": AUTH0_CLIENT_ID,
            "email": user.email,
            "password": user.password,
            "username":user.username,
            "connection": "Username-Password-Authentication",
            "email_verified": False,
            "user_metadata": {
                "firstName": user.firstName,
                "lastName": user.lastName,
                "gender": user.gender,
                "phone": user.phone,
                "birthDate": user.birthDate,
                "status":"active"
            }
        },
        headers={"content-type": "application/json"},
    )
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return {"detail":"Resistration successful"}


def login(login_input:LoginInput,db:Session):

    if not login_input.email:
        raise HTTPException(status_code=422, detail="Email field is missing")
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, login_input.email):
        raise HTTPException(status_code=400, detail="Invalid email")
    if not login_input.password:
        raise HTTPException(status_code=422, detail="Password field is missing")

    response = requests.post(
        f"https://{AUTH0_DOMAIN}/oauth/token",
        json={
        "grant_type": "password",
        "username": login_input.email,
        "password": login_input.password,
        "audience": API_AUDIENCE,
        "connection": "Username-Password-Authentication",
        "scope": "openid profile email",
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET
        },
        headers={"content-type": "application/json"}
    )
    if response.status_code != 200:
        raise HTTPException(status_code=401, detail=response.json()["error_description"])
    decoded_token = verify_token(response.json()["access_token"])
    role = decoded_token["role"]
    user_id = decoded_token["user_id"]
    add_log(user_id=user_id,log_name="Login",description="User logged in successfully",db=db)
    return {"detail":"Login successful","access_token": response.json()["access_token"],"id_token":response.json()["id_token"]}



def get_user_info(token,db:Session):
    decoded_token = verify_token(token.credentials)
    if not decoded_token:
        raise HTTPException(status_code=401, detail="Token invalid")
    response  = requests.get(f"https://{AUTH0_DOMAIN}/userinfo", headers={"content-Type": "application/json", "Authorization": f"Bearer {token.credentials}"})
    user_id = decoded_token["user_id"]
    db_logs = Activity_Logs(user_id=user_id,log_name="User Info",description="User info requested")
    db.add(db_logs)
    db.commit()
    db.refresh(db_logs)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    
    return {"detail":"Successful","data":response.json()}

def user_partial_update(userId: str,token,user: UserPartial,db: Session):
    decoded_token = verify_token(token.credentials)
    if not decoded_token:
        raise HTTPException(status_code=401, detail="Token invalid")
    role = decoded_token["role"]
    user_id = decoded_token["user_id"]
    if role!="admin" and user_id!=userId:
        raise HTTPException(status_code=401, detail="Unauthorized")
    payload = {
        "user_metadata":{}
    }
    if user.firstName:
        payload["user_metadata"]["firstName"] = user.firstName
    if user.lastName:
        payload["user_metadata"]["lastName"] = user.lastName
    if user.gender:
        payload["user_metadata"]["gender"] = user.gender
    if user.phone:
        payload["user_metadata"]["phone"] = user.phone
    if user.birthDate:
        payload["user_metadata"]["birthDate"] = user.birthDate
    if user.email:
        payload["email"] = user.email
    if user.password:
        payload["password"] = user.password
    if user.username:
        payload["username"] = user.username
    if user.nickname:
        payload["nickname"] = user.nickname
    if user.addresses:
        addresses = [address.dict() for address in user.addresses]
        payload["user_metadata"]["addresses"] = addresses
    if not payload["user_metadata"]:
        payload.pop("user_metadata")
    response  = requests.patch(f"https://{AUTH0_DOMAIN}/api/v2/users/{userId}",json=payload ,headers={"content-Type": "application/json", "Authorization": f"Bearer {token.credentials}"})
    if response.status_code != 200:
    
        raise HTTPException(status_code=response.status_code, detail=response.text)
    add_log(user_id=user_id,log_name="Partial User Update",description=f"User update requested",db=db)
    return {"detail":"Successfully updated","data":response.json()}

def get_a_user_info(userId,token,db:Session):
    decoded_token = verify_token(token.credentials)
    if not decoded_token:
        raise HTTPException(status_code=401, detail="Token invalid")
    role = decoded_token["role"]
    user_id = decoded_token["user_id"]
    if role!="admin" and user_id!=userId:
        raise HTTPException(status_code=401, detail="Unauthorized")
    


    response  = requests.get(f"https://{AUTH0_DOMAIN}/api/v2/users/{userId}",headers={"content-Type": "application/json", "Authorization": f"Bearer {token.credentials}"})
    if response.status_code != 200:
    
        raise HTTPException(status_code=response.status_code, detail=response.text)
    add_log(user_id=user_id,log_name="Get a User Info",description=f"User Info requested",db=db)
    return {"detail":"Successful","data":response.json()}


def delete_user(userId,token,db: Session):
    decoded_token = verify_token(token.credentials)
    if not decoded_token:
        raise HTTPException(status_code=401, detail="Token invalid")
    role = decoded_token["role"]
    user_id = decoded_token["user_id"]
    if role!="admin" and user_id!=userId:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    response  = requests.patch(f"https://{AUTH0_DOMAIN}/api/v2/users/{userId}",json={
        "user_metadata":{
        "status":"closed"
        }
    },headers={"content-Type": "application/json", "Authorization": f"Bearer {token.credentials}"})
    if response.status_code != 200:
    
        raise HTTPException(status_code=response.status_code, detail=response.text)
    add_log(user_id=user_id,log_name="Delete User",description=f"User Account closed",db=db)
    return {"detail":"User deleted successfully"}


def password_reset(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    # Check if the email matches the pattern
    if not re.match(pattern, email):
        raise HTTPException(status_code=400, detail="Invalid email")

    response_token = requests.post(
        f"https://{AUTH0_DOMAIN}/oauth/token",
        json={
        "grant_type": "client_credentials",
        "audience": API_AUDIENCE,
        "connection": "Username-Password-Authentication",
        "scope": "openid profile email",
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET
        },
        headers={"content-type": "application/json"}
    )
    if response_token.status_code != 200:
    
        raise HTTPException(status_code=response_token.status_code, detail=response_token.text)
    
    access_token = response_token.json()["access_token"]
    response  = requests.post(f"https://{AUTH0_DOMAIN}/api/v2/tickets/password-change",json={
        "email":email,
        "connection_id":AUTH0_CONNECTION_ID
        }
    ,headers={"content-Type": "application/json", "Authorization": f"Bearer {access_token}"})
    if response.status_code != 201:
    
        raise HTTPException(status_code=response.status_code, detail=response.text)
    url = response.json()["ticket"]
    send_password_reset_email(user_email=email,url=url)
    return {"detail": "Password reset email sent successfully"}


def get_users(limit, offset,token,db: Session):
    decoded_token = verify_token(token.credentials)
    if not decoded_token:
        raise HTTPException(status_code=401, detail="Token invalid")
    role = decoded_token["role"]
    user_id = decoded_token["user_id"]
    if role!="admin":
        raise HTTPException(status_code=401, detail="Unauthorized")
    params = {
    "per_page": min(limit, 100),  # the number of results per page, limited to 1000 at most
    "page": offset,  # the page number to return
}
    response  = requests.get(f"https://{AUTH0_DOMAIN}/api/v2/users"
    ,headers={"content-Type": "application/json", "Authorization": f"Bearer {token.credentials}"},params=params)

    add_log(user_id=user_id,log_name="Get all Users", description="All users requested",db=db)
    if response.status_code != 200:
    
        raise HTTPException(status_code=response.status_code, detail=response.text)
    
    return {"detail":"Successful","data":response.json()}

def create_user(token,user: UserPartial, db: Session):
    decoded_token = verify_token(token.credentials)
    if not decoded_token:
        raise HTTPException(status_code=401, detail="Token invalid")
    role = decoded_token["role"]
    user_id = decoded_token["user_id"]
    if role!="admin":
        raise HTTPException(status_code=401, detail="Unauthorized")
    payload = {
        "connection": "Username-Password-Authentication",
        "user_metadata":{
            "status":"active"
        }
        
    }

    if not user.email:
        raise HTTPException(status_code=422, detail="Email field is missing")
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    # Check if the email matches the pattern
    if not re.match(pattern, user.email):
        raise HTTPException(status_code=400, detail="Invalid email")
    if not user.password:
        raise HTTPException(status_code=422, detail="Password field is missing")
    if user.firstName:
        payload["user_metadata"]["firstName"] = user.firstName
    if user.lastName:
        payload["user_metadata"]["lastName"] = user.lastName
    if user.gender:
        payload["user_metadata"]["gender"] = user.gender
    if user.phone:
        payload["user_metadata"]["phone"] = user.phone
    if user.birthDate:
        payload["user_metadata"]["birthDate"] = user.birthDate
    if user.email:
        payload["email"] = user.email
    if user.password:
        payload["password"] = user.password
    if user.username:
        payload["username"] = user.username
    if user.nickname:
        payload["nickname"] = user.nickname
    
    response  = requests.post(f"https://{AUTH0_DOMAIN}/api/v2/users",json=payload ,headers={"content-Type": "application/json", "Authorization": f"Bearer {token.credentials}"})

    add_log(user_id=user_id,log_name="Create a User", description="Creating a user requested",db=db)

    if response.status_code != 201:
    
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return {"detail":"User created successfully","data":response.json()} 


def get_user_logs(userId:str,token,db: Session):
    """Get user logs with the access token"""
    decoded_token = verify_token(token.credentials)
    if not decoded_token:
        raise HTTPException(status_code=401, detail="Token invalid")
    role = decoded_token["role"]
    user_id = decoded_token["user_id"]
    if role!="admin":
        raise HTTPException(status_code=401, detail="Unauthorized")
    logs = db.query(Activity_Logs).filter(Activity_Logs.user_id == userId).all()
    if not logs:
        raise HTTPException(status_code=400, detail="User id invalid")
    return logs

def login_with_external_identity_provider(request,connection: str):
    return {"detail":"Successful","url":f"https://{AUTH0_DOMAIN}/authorize?response_type=code&client_id={AUTH0_CLIENT_ID}&redirect_uri={AUTH0_CALLBACK_URL}&connection={connection}"}

def callback(request,code: str,state:str = None):
    headers = {'content-type': 'application/json'}
    data = {
        'grant_type': 'authorization_code',
        'client_id': AUTH0_CLIENT_ID,
        'client_secret': AUTH0_CLIENT_SECRET,
        "scope": "openid profile email",
        'code': code,
        'redirect_uri': AUTH0_CALLBACK_URL
    }
    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    token_info = requests.post(token_url, headers=headers, json=data).json()
    access_token = token_info['access_token']
    print(access_token)
    user_info_url = f"https://{AUTH0_DOMAIN}/userinfo"
    headers = {'authorization': f"Bearer {access_token}"}
    user_info = requests.get(user_info_url, headers=headers).json()
    return user_info
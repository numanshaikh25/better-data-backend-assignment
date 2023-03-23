from fastapi import Depends, FastAPI, Response, Request,status, HTTPException,Header ,Body, APIRouter
from app.models import User,UserPartial,LoginInput, LoginResponse, Password_Reset
from app.services import user_services
from sqlalchemy.orm import Session
from database.db import get_db
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import EmailStr
from typing import List, Optional

# Define the custom header name
AUTH_HEADER_NAME = "Authorization"

# Define the HTTPBearer authentication scheme
http_bearer = HTTPBearer()

router = APIRouter()


@router.post("/register")
def register(user: User = Body(...)):
    """Registers a new user and sends a confirmation email"""
    return user_services.register(user)
    

@router.post("/login")
def login(login_input: LoginInput = Body(...),db: Session= Depends(get_db)):
    """Login's a user and sends access token and id token"""
    return user_services.login(login_input,db)

@router.get("/info")
def get_user_info(token: HTTPAuthorizationCredentials = Depends(http_bearer),db: Session= Depends(get_db)):
    """Get user info with the access token"""
    return user_services.get_user_info(token,db)

@router.patch("/{userId}")
def user_partial_update(userId: str,token: HTTPAuthorizationCredentials = Depends(http_bearer),user: UserPartial = Body(...),db: Session= Depends(get_db)):
    """Update a user partially using an access token"""
    return user_services.user_partial_update(userId,token,user,db)

@router.get("/{userId}")
def get_a_user_info(userId: str,token: HTTPAuthorizationCredentials = Depends(http_bearer),db: Session= Depends(get_db)):
    """Get a particular user's info with the help of access token"""
    return user_services.get_a_user_info(userId,token,db)

@router.delete("/{userId}")
def delete_user(userId: str,token: HTTPAuthorizationCredentials = Depends(http_bearer),db: Session= Depends(get_db)):
    """Delete your own account or admin can delete another user's account"""
    return user_services.delete_user(userId,token,db)

@router.post("/password-reset")
def password_reset(email:Password_Reset = Body(...)):
    """Request password reset link if you have forgotten password"""
    return user_services.password_reset(email.email)


@router.get("")
def get_users(limit:Optional[int] = 1000, offset: Optional[int] = 0,token: HTTPAuthorizationCredentials = Depends(http_bearer),db: Session= Depends(get_db)):
    """Get all users, only admin can access"""
    return user_services.get_users(limit,offset,token,db)

@router.post("")
def create_user(token: HTTPAuthorizationCredentials = Depends(http_bearer),user: UserPartial = Body(...),db: Session= Depends(get_db)):
    """Create a user, only admin can access"""
    return user_services.create_user(token,user,db)


@router.get("/logs/{userId}")
def get_user_logs(userId:str,token: HTTPAuthorizationCredentials = Depends(http_bearer),db: Session= Depends(get_db)):
    """Get user's logs, only admin can access"""
    return user_services.get_user_logs(userId,token,db)


@router.get("/login/{connection}")
async def login_with_external_identity_provider(request: Request, connection: str):
    return user_services.login_with_external_identity_provider(request,connection)

@router.get("/callback")
async def callback(request: Request, code: str, state: str = None):
    return user_services.callback(request,code,state)
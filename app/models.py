from typing import List, Optional
from pydantic import BaseModel,EmailStr


class Address(BaseModel):
    address: str
    city: str
    postalCode: str
    state: str
    primary: bool
    label: str


class User(BaseModel):
    firstName: Optional[str]
    lastName: Optional[str]
    gender: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    username: Optional[str]
    password: Optional[str]
    birthDate: Optional[str]

class UserPartial(BaseModel):
    nickname: Optional[str]
    firstName: Optional[str]
    lastName: Optional[str]
    gender: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    username: Optional[str]
    password: Optional[str]
    birthDate: Optional[str]
    addresses: Optional[List[Address]]


class LoginInput(BaseModel):
    email: Optional[EmailStr]
    password: Optional[str]


class LoginResponse(BaseModel):
    detail: str
    access_token: str
    id_token: str


class Password_Reset(BaseModel):

    email: Optional[str]
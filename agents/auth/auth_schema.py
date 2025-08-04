# from pydantic import BaseModel, EmailStr

# class LoginRequest(BaseModel):
#     email: EmailStr
#     password: str

# class LoginResponse(BaseModel):
#     access_token: str
#     token_type: str = "bearer"

from pydantic import BaseModel, EmailStr
from typing import Optional

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    email: EmailStr
    is_active: bool = True

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None

class TokenData(BaseModel):
    email: Optional[str] = None
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    username: str
    name: str
    email: EmailStr
    avatar_url: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    avatar_url: Optional[str] = None
    password: Optional[str] = None
    username: Optional[str] = None


class UserOut(UserBase):
    id: int
    last_login_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class UserAuthOut(UserOut):
    token: str

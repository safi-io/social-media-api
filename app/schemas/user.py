from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    username: str
    name: str
    email: str
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

    class Config:
        orm_mode = True


class UserAuthOut(BaseModel):
    id: int
    username: str
    name: str
    email: str

    token: str
    token_type: str = "bearer"

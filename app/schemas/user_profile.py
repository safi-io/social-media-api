from typing import List, Optional, Dict
from pydantic import BaseModel, HttpUrl

from app.schemas.user import UserOut


class UserProfileBase(BaseModel):
    title: Optional[str] = None
    bio: Optional[str] = None
    skills: Optional[List[str]] = []
    cover_image_url: Optional[HttpUrl] = None
    location: Optional[str] = None
    external_urls: Optional[Dict[str, HttpUrl]] = {}
    profile_strength: Optional[int] = 0


class UserProfileCreate(UserProfileBase):
    user_id: int


class UserProfileUpdate(BaseModel):
    title: Optional[str] = None
    bio: Optional[str] = None
    skills: Optional[List[str]] = None
    cover_image_url: Optional[HttpUrl] = None
    location: Optional[str] = None
    external_urls: Optional[Dict[str, HttpUrl]] = None
    profile_strength: Optional[int] = None


class UserProfileOut(UserProfileBase):
    user_id: int

    class Config:
        orm_mode = True


class UserProfileWithUser(UserProfileOut):
    user: UserOut

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class PostBase(BaseModel):
    content: Optional[str] = None
    tags: Optional[List[str]] = []


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    content: Optional[str] = None
    tags: Optional[List[str]] = None


class PostImageResponse(BaseModel):
    image_url: str

    class Config:
        from_attributes = True


class PostResponse(PostBase):
    id: int
    user_id: int
    analytics: dict
    images: List[PostImageResponse]
    created_at: datetime

    class Config:
        from_attributes = True


class PostCommentCreate(BaseModel):
    content: str


class PostCommentResponse(BaseModel):
    id: int
    user_id: int
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

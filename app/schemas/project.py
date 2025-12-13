from datetime import datetime
from typing import Optional, Dict

from pydantic import BaseModel

from app.models.project import ProjectStatusEnum, VisibilityStatusEnum


class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None

    status: Optional[ProjectStatusEnum] = ProjectStatusEnum.PENDING

    visibility: Optional[VisibilityStatusEnum] = VisibilityStatusEnum.PUBLIC

    external_urls: Optional[Dict] = {
        "github_url": None,
        "live_demo_url": None,
        "cloudinary_url": None
    }

    analytics: Optional[Dict] = {
        "bookmarks_count": 0,
        "views_count": 0
    }

    tech_stack: Optional[list[str]] = []
    assignments: Optional[Dict[str, str]] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ProjectStatusEnum] = None
    visibility: Optional[VisibilityStatusEnum] = None
    external_urls: Optional[Dict] = None
    analytics: Optional[Dict] = None
    tech_stack: Optional[list[str]] = None
    assignments: Optional[Dict[str, str]] = None

    class Config:
        from_attributes = True


class Project(ProjectBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        extra = "ignore"


class ProjectDelete(BaseModel):
    project_id: int

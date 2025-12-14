from fastapi import APIRouter

router = APIRouter()

# Auth
from app.api.v1.auth import router as auth_router

router.include_router(auth_router, prefix="/auth", tags=["Authentication"])

# Users
from app.api.v1.user import router as user_router

router.include_router(user_router, prefix="/users", tags=["User"])

# Follows

from app.api.v1.follow import router as follow_router

router.include_router(follow_router, prefix="/follows", tags=["Follows"])

# Project

from app.api.v1.project import router as project_router

router.include_router(project_router, prefix="/projects", tags=["Projects"])

# Websockets
from app.api.v1.websockets import router as websockets_router

router.include_router(websockets_router, prefix="/ws", tags=["Websockets"])

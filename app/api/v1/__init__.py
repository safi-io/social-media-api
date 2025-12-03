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

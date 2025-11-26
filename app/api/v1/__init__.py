from fastapi import APIRouter

router = APIRouter()

# Users
from app.api.v1.user import router as user_router

router.include_router(user_router, prefix="/users")

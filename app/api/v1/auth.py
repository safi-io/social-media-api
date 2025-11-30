from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User as user_model
from app.schemas.user import UserCreate

router = APIRouter()


@router.post("signup", response_model=UserCreate, summary="Creates a New User.")
def sign_up():
    pass

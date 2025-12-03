from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.user import User as user_model
from app.models.user_profile import UserProfile as user_profile_model
from app.schemas.user import UserCreate, UserOut, UserAuthOut
from app.services.create_access_token import create_access_token
from app.services.password_hash import *
import re

router = APIRouter()


@router.post("/signup", response_model=UserOut, summary="Creates a New User & User Profile.")
def sign_up(new_user: UserCreate, db: Session = Depends(get_db)):
    # Convert pydantic model to dict
    new_user_data = new_user.model_dump(exclude_unset=True)

    # Check for empty fields
    for key, value in new_user_data.items():
        if value is None or str(value).strip() == "":
            raise HTTPException(
                status_code=400,
                detail=f"{key.capitalize()} cannot be empty."
            )

        # Trim strings
        if isinstance(value, str):
            new_user_data[key] = value.strip()

    # Check if username already exists
    if db.query(user_model).filter(user_model.username == new_user.username).first():
        raise HTTPException(
            status_code=400,
            detail="Username already exists."
        )

    # Check if email already exists
    if db.query(user_model).filter(user_model.email == new_user.email).first():
        raise HTTPException(
            status_code=400,
            detail="Email already exists."
        )

    # Validations for Email, Username, and Password
    for key, value in new_user_data.items():

        # Matching Email Pattern
        if key == "email":
            if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid email format",
                )

        # Checking Username Length
        if key == "username" and len(value) < 4:
            raise HTTPException(
                status_code=400,
                detail="Username must be at-least 4 characters."
            )

        # Checking password Length
        if key == "password" and len(value) < 8:
            raise HTTPException(
                status_code=400,
                detail="Password must be at-least 8 characters."
            )

    # Hash the password and replace original
    new_user_data["hashed_password"] = get_password_hash(new_user_data.pop("password"))

    try:
        # Create user
        user = user_model(**new_user_data)
        db.add(user)
        db.flush()  # assign user.id

        # Create profile
        user_profile = user_profile_model(user_id=user.id)
        db.add(user_profile)

        # Commit both
        db.commit()
    except:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create user")

    return user


@router.post(
    "/login",
    response_model=UserAuthOut, summary="Login's a User using Username/Email and Return JWT.",
    description="OAuth2PasswordRequestForm uses form data (application/x-www-form-urlencoded) instead of raw JSON.")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    login_id = form_data.username  # Could be username or email
    password = form_data.password

    # Filtering on Username and Email
    user = db.query(user_model).filter(
        or_(user_model.email == login_id, user_model.username == login_id)
    ).first()

    # Verifying the Hash
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Creating an Access Token
    access_token_expires = timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )

    return UserAuthOut(
        token=access_token,
        id=user.id,
        username=user.username,
        email=user.email,
        name=user.name,
    )

from typing import Any
from pydantic import HttpUrl

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.db.session import get_db
from app.models.user import User as user_model
from app.models.user_profile import UserProfile as user_profile
from app.schemas.user_profile import UserProfileWithUser
from app.services.cloudinary import upload_image
from app.services.get_current_user import get_current_user
from app.services.validate_image import validate_image

router = APIRouter()


@router.post("/upload-profile-picture", summary="Uploads User's Profile Picture.")
def upload_picture(
        profile_image: UploadFile = File(...),
        current_user=Depends(get_current_user),
        db: Session = Depends(get_db)
):
    validate_image(profile_image)
    url = upload_image(profile_image, "user_profile_images")

    current_user.avatar_url = url

    db.commit()
    db.refresh(current_user)

    return {
        "message": "Profile picture updated",
        "profile_image": current_user.avatar_url
    }


@router.post("/upload-cover-image", summary="Uploads User's Cover Picture.")
def upload_picture(
        cover_image: UploadFile = File(...),
        current_user=Depends(get_current_user),
        db: Session = Depends(get_db)
):
    validate_image(cover_image)
    url = upload_image(cover_image, "user_cover_images")

    get_user_profile = db.query(user_profile).filter(user_profile.user_id == current_user.id).first()
    get_user_profile.cover_image_url = url

    db.commit()
    db.refresh(get_user_profile)

    return {
        "message": "Cover Image Updated",
        "profile_image": get_user_profile.cover_image_url
    }


@router.get("/get/me", response_model=UserProfileWithUser)
def get_profile_with_user(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    profile = (
        db.query(user_profile)
        .options(joinedload(user_profile.user))
        .filter(user_profile.user_id == current_user.id)
        .first()
    )
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.get("/get/{user_id}", response_model=UserProfileWithUser)
def get_profile_with_user(user_id: int, db: Session = Depends(get_db)):
    profile = (
        db.query(user_profile)
        .options(joinedload(user_profile.user))
        .filter(user_profile.user_id == user_id)
        .first()
    )
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.get("/get-all-users", summary="Returning All Users")
def user_all(db: Session = Depends(get_db), current_user=Depends(get_current_user), ):
    return db.query(user_model).all()


@router.get("/get-all-not-followed-users", summary="Return all users not yet followed by the current user.")
def user_all(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    followed_ids = [user.id for user in current_user.followings]

    users_not_followed = db.query(user_model).filter(
        user_model.id != current_user.id,
        ~user_model.id.in_(followed_ids)
    ).all()

    return users_not_followed


from app.schemas.user_profile import UserProfileUpdate, UserProfileWithUser


@router.patch(
    "/update",
    response_model=UserProfileWithUser,
    summary="Update current user's profile"
)
def update_my_profile(
        payload: UserProfileUpdate,
        current_user=Depends(get_current_user),
        db: Session = Depends(get_db)
):
    profile = (
        db.query(user_profile)
        .filter(user_profile.user_id == current_user.id)
        .first()
    )

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    update_data = payload.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(status_code=400, detail="No data provided to update")

    for key, value in update_data.items():
        setattr(profile, key, normalize_for_db(value))

    db.commit()
    db.refresh(profile)

    return profile


def normalize_for_db(value: Any):
    if isinstance(value, HttpUrl):
        return str(value)

    if isinstance(value, dict):
        return {k: normalize_for_db(v) for k, v in value.items()}

    if isinstance(value, list):
        return [normalize_for_db(v) for v in value]

    return value

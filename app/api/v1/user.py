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

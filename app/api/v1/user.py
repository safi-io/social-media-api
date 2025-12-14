from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User as user_model
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


@router.get("/get-all-users", summary="Returning All Users")
def user_all(db: Session = Depends(get_db), current_user=Depends(get_current_user),):
    return db.query(user_model).all()

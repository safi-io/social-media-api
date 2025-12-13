import logging

import cloudinary
import cloudinary.uploader
from fastapi import UploadFile

from app.core.config import settings

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True
)

logger = logging.getLogger(__name__)


def upload_image(file: UploadFile, folder_name: str) -> str:
    try:
        result = cloudinary.uploader.upload(
            file.file,
            folder=folder_name,
            resource_type="image"
        )
        return result["secure_url"]
    except Exception as e:
        logger.exception("Cloudinary upload failed")
        raise

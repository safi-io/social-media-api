from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User as user_model

router = APIRouter()


@router.get("/me", summary="Returning User's Own Data")
def user_me():
    return {"Status": "It's You :)"}


@router.get("/get-all-users", summary="Returning All Users")
def user_all(db: Session = Depends(get_db)):
    return db.query(user_model).all()

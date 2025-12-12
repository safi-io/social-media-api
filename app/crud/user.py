from sqlalchemy.orm import Session

import app.models.user as user_model
import app.schemas.user as user_schema


def create_user(db: Session, user: user_schema.UserCreate):
    db_user = user_model.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(user_model.User).offset(skip).limit(limit).all()

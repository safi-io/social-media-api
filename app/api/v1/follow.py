from fastapi import APIRouter, Depends, HTTPException

from app.schemas.follow import FollowMinimal, FollowRequest
from app.services.get_current_user import get_current_user

from app.db.session import get_db
from app.models.follow import Follow as follow_model
from app.models.user import User as user_model
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/following", response_model=list[FollowMinimal])
def get_following(current_user=Depends(get_current_user)):
    return current_user.followings


@router.get("/followers", response_model=list[FollowMinimal])
def get_followers(current_user=Depends(get_current_user)):
    return current_user.followers


@router.post("/add-following")
def add_followers(
        data: FollowRequest,
        current_user=Depends(get_current_user),
        db: Session = Depends(get_db)):
    if not db.query(user_model).filter(user_model.id == data.beta_user_id).first():
        raise HTTPException(status_code=400, detail="Unable to Find the Next User.")

    if current_user.id == data.beta_user_id:
        raise HTTPException(status_code=400, detail="You can't Follow Yourself.")

    try:

        follow_req = follow_model(
            follower_id=current_user.id,
            following_id=int(data.beta_user_id)
        )
        db.add(follow_req)
        db.commit()

        return {"message": "Followed successfully."}

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to follow the user."
        )


@router.post("/remove-following")
def remove_following(data: FollowRequest,
                     current_user=Depends(get_current_user),
                     db: Session = Depends(get_db)):
    if not db.query(user_model).filter(user_model.id == data.beta_user_id).first():
        raise HTTPException(status_code=400, detail="Unable to Find the Next User.")

    if current_user.id == data.beta_user_id:
        raise HTTPException(status_code=400, detail="Same User.")

    deleted = db.query(follow_model).filter(
        follow_model.follower_id == current_user.id,
        follow_model.following_id == data.beta_user_id
    ).delete()

    if deleted == 0:
        raise HTTPException(status_code=404, detail="You are not following this user.")

    db.commit()

    return {"message": "Unfollowed successfully."}


@router.post("/remove-follower")
def remove_follower(data: FollowRequest,
                    current_user=Depends(get_current_user),
                    db: Session = Depends(get_db)):
    if not db.query(user_model).filter(user_model.id == data.beta_user_id).first():
        raise HTTPException(status_code=400, detail="Unable to Find the User.")

    if current_user.id == data.beta_user_id:
        raise HTTPException(status_code=400, detail="Same User.")

    # Delete the follower relationship
    deleted = db.query(follow_model).filter(
        follow_model.follower_id == data.beta_user_id,
        follow_model.following_id == current_user.id
    ).delete()

    db.commit()

    if deleted == 0:
        raise HTTPException(status_code=404, detail="This user is not following you.")

    return {"message": "Follower removed successfully."}

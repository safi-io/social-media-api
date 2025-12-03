from fastapi import APIRouter, Depends, HTTPException

from app.schemas.follow import FollowMinimal, FollowRequest
from app.services.get_current_user import get_current_user

from app.db.session import get_db
from app.models.follow import Follow as follow_model
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/following", response_model=list[FollowMinimal])
def get_following(current_user=Depends(get_current_user)):
    return current_user.followings


@router.get("/followers", response_model=list[FollowMinimal])
def get_following(current_user=Depends(get_current_user)):
    return current_user.followers


@router.post("/add-follower")
def add_followers(
        data: FollowRequest,
        current_user=Depends(get_current_user),
        db: Session = Depends(get_db)):
    if current_user.id == data.beta_user_id:
        raise HTTPException(status_code=400, detail="You can't Follow Yourself.")

    try:
        follow_req = follow_model(follower_id=current_user.id, following_id=int(data.beta_user_id))
        db.add(follow_req)
        db.commit()
    except:
        raise HTTPException(status_code=500, detail="Failed to follow the User.")

    return {"status": f"Followed USER ID: {data.beta_user_id}"}

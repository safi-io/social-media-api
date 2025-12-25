import json

from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy import or_, func
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.follow import Follow
from app.models.post import Post
from app.models.post_comment import PostComment
from app.models.post_image import PostImage
from app.models.post_like import PostLike
from app.schemas.post import (
    PostCreate, PostUpdate, PostResponse,
    PostCommentCreate, PostCommentResponse
)
from app.services.cloudinary import upload_image
from app.services.get_current_user import get_current_user
from sqlalchemy.orm.attributes import flag_modified

router = APIRouter(prefix="/posts", tags=["Posts"])


# CREATE POST
@router.post("/create", response_model=PostResponse)
def create_post(
        data: str = Form(...),
        images: list[UploadFile] | None = File(None),
        current_user=Depends(get_current_user),
        db: Session = Depends(get_db)
):
    payload = PostCreate(**json.loads(data))

    post = Post(
        user_id=current_user.id,
        content=payload.content,
        tags=payload.tags
    )
    db.add(post)
    db.flush()

    if images:
        folder = f"posts/{post.id}"
        for img in images:
            url = upload_image(img, folder)
            db.add(PostImage(post_id=post.id, image_url=url))

    db.commit()
    db.refresh(post)
    return post


# UPDATE POST
@router.put("/{post_id}", response_model=PostResponse)
def update_post(
        post_id: int,
        payload: PostUpdate,
        current_user=Depends(get_current_user),
        db: Session = Depends(get_db)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(404, "Post not found")

    if post.user_id != current_user.id:
        raise HTTPException(403, "Not allowed")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(post, key, value)

    db.commit()
    return post


# DELETE POST
@router.delete("/{post_id}")
def delete_post(
        post_id: int,
        current_user=Depends(get_current_user),
        db: Session = Depends(get_db)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(404, "Post not found")

    if post.user_id != current_user.id:
        raise HTTPException(403, "Not allowed")

    db.delete(post)
    db.commit()
    return {"message": "Deleted successfully"}


@router.post("/{post_id}/like")
def toggle_like(post_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    current_user_id = current_user.id

    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    existing_like = db.query(PostLike).filter(
        PostLike.post_id == post_id,
        PostLike.user_id == current_user_id
    ).first()

    if existing_like:
        # Unlike
        db.delete(existing_like)
        post.analytics['likes_count'] = max(post.analytics.get('likes_count', 1) - 1, 0)
        action = "unliked"
    else:
        # Like
        new_like = PostLike(post_id=post_id, user_id=current_user_id)
        db.add(new_like)
        post.analytics['likes_count'] = post.analytics.get('likes_count', 0) + 1
        action = "liked"

    flag_modified(post, "analytics")  # <-- This is crucial
    post.updated_at = func.now()
    db.commit()
    db.refresh(post)

    return {
        "status": "ok",
        "action": action,
        "likes_count": post.analytics['likes_count']
    }


# COMMENTS
@router.post("/{post_id}/comment", response_model=PostCommentResponse)
def add_comment(
        post_id: int,
        payload: PostCommentCreate,
        current_user=Depends(get_current_user),
        db: Session = Depends(get_db)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Add comment
    comment = PostComment(
        post_id=post_id,
        user_id=current_user.id,
        content=payload.content
    )
    db.add(comment)

    # Update analytics
    post.analytics['comments_count'] = post.analytics.get('comments_count', 0) + 1
    flag_modified(post, "analytics")  # mark JSON as modified
    post.updated_at = func.now()

    db.commit()
    db.refresh(comment)

    return comment


@router.get("/feed", response_model=list[PostResponse])
def get_feed(
        limit: int = 10,
        offset: int = 0,
        current_user=Depends(get_current_user),
        db: Session = Depends(get_db)
):
    followed_users_query = (
        db.query(Follow.following_id)
        .filter(Follow.follower_id == current_user.id)
    )

    posts = (
        db.query(Post)
        .filter(
            or_(
                Post.user_id.in_(followed_users_query),
                Post.user_id == current_user.id
            )
        )
        .order_by(Post.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return posts


@router.get("/{post_id}/comments", response_model=list[PostCommentResponse])
def get_comments(
        post_id: int,
        limit: int = 20,
        offset: int = 0,
        current_user=Depends(get_current_user),
        db: Session = Depends(get_db)
):
    comments = (
        db.query(PostComment)
        .filter(PostComment.post_id == post_id)
        .order_by(PostComment.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    return comments


@router.get("/user/{user_id}", response_model=list[PostResponse])
def get_user_posts(
        user_id: int,
        limit: int = 10,
        offset: int = 0,
        current_user=Depends(get_current_user),
        db: Session = Depends(get_db)
):
    posts = (
        db.query(Post)
        .filter(Post.user_id == user_id)
        .order_by(Post.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return posts


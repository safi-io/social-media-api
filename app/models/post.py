from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy.orm import relationship

from app.db.session import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)

    content = Column(String, nullable=True)
    tags = Column(ARRAY(String), default=list)

    analytics = Column(
        JSONB,
        default=lambda: {
            "likes_count": 0,
            "comments_count": 0,
            "views_count": 0
        }
    )

    images = relationship(
        "PostImage",
        back_populates="post",
        cascade="all, delete-orphan"
    )

    likes = relationship(
        "PostLike",
        cascade="all, delete-orphan"
    )

    comments = relationship(
        "PostComment",
        cascade="all, delete-orphan"
    )

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

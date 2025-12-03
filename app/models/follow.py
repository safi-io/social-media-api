from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.db.session import Base


class Follow(Base):
    __tablename__ = "follows"

    follower_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )

    following_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )

    created_at = Column(
        DateTime,
        server_default=func.now(),
        index=True,
    )

    # The User who is following
    follower = relationship(
        "User",
        foreign_keys=[follower_id],
        back_populates="_following_relationships"
    )

    # The User being followed
    following = relationship(
        "User",
        foreign_keys=[following_id],
        back_populates="_follower_relationships"
    )

    def __repr__(self):
        return f"<Follower ID: {self.follower_id} | Following ID: {self.following_id}>"

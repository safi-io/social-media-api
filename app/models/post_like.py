from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from app.db.session import Base


class PostLike(Base):
    __tablename__ = "post_likes"

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    __table_args__ = (
        UniqueConstraint("post_id", "user_id", name="unique_post_like"),
    )

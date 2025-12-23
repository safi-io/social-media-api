from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from app.db.session import Base


class PostComment(Base):
    __tablename__ = "post_comments"

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    content = Column(String, nullable=False)

    created_at = Column(DateTime, server_default=func.now())

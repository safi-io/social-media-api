from sqlalchemy import Column, Integer, String, DateTime, func
from app.db.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    address = Column(String)
    created_at = Column(DateTime, server_default=func.now())

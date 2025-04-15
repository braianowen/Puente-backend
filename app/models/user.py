# app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean
from app.db.database import Base

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "trading_schema"}
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
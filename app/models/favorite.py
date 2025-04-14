# backend/app/models/favorite.py
from sqlalchemy import Column, Integer, ForeignKey, String
from app.db.database import Base

class Favorite(Base):
    __tablename__ = "favorites"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    symbol = Column(String)  
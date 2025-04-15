# backend/app/models/favorite.py
from sqlalchemy import Column, Integer, ForeignKey, String
from app.db.database import Base

class Favorite(Base):
    __tablename__ = "favorites"
    __table_args__ = {"schema": "trading_schema"}
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("trading_schema.users.id"))
    symbol = Column(String)  
# backend/app/schemas/favorite.py
from pydantic import BaseModel

class FavoriteCreate(BaseModel):
    symbol: str

class FavoriteResponse(BaseModel):
    id: int
    symbol: str
    user_id: int

    class Config:
        orm_mode = True
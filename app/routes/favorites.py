# backend/app/routes/favorites.py
from fastapi import APIRouter, Depends, HTTPException, status
from requests import Session
from app.db.database import get_db
from app.models.favorite import Favorite
from app.models.user import User
from app.schemas.favorite import FavoriteCreate, FavoriteResponse
from app.core.security import get_current_user

router = APIRouter(tags=["Favorites"])

@router.post("/favorites", response_model=FavoriteResponse)
def add_favorite(
    favorite: FavoriteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verificar si ya existe
    existing = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.symbol == favorite.symbol
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El instrumento ya está en favoritos"
        )
    
    new_favorite = Favorite(
        user_id=current_user.id,
        symbol=favorite.symbol
    )
    
    db.add(new_favorite)
    db.commit()
    db.refresh(new_favorite)
    
    return new_favorite

@router.delete("/favorites/{symbol}", status_code=status.HTTP_204_NO_CONTENT)
def remove_favorite(
    symbol: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    favorite = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.symbol == symbol
    ).first()
    
    if not favorite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Favorito no encontrado"
        )
    
    db.delete(favorite)
    db.commit()
# backend/app/routes/instruments.py (actualizado)
from fastapi import APIRouter, Depends, HTTPException
from app.models.user import User
from app.services.alpha_vantage import AlphaVantageService
from app.core.security import get_current_user

router = APIRouter(tags=["Instruments"])
alpha_vantage = AlphaVantageService()

@router.get("/instruments/{symbol}")
def get_instrument(symbol: str, current_user: User = Depends(get_current_user)):
    data = alpha_vantage.get_global_quote(symbol)
    if not data:
        raise HTTPException(status_code=404, detail="Instrumento no encontrado")
    
    return {
        "symbol": symbol,
        "price": data.get("05. price"),
        "change": data.get("09. change"),
        "change_percent": data.get("10. change percent")
    }
# backend/app/routes/instruments.py
from fastapi import APIRouter, HTTPException
from app.services.market_service import MarketDataService
from typing import Optional

router = APIRouter(tags=["Instruments"])
market_service = MarketDataService()

@router.get("/instruments/{symbol}")
def get_instrument(symbol: str):
    data = market_service.get_instrument_data(symbol)
    if not data:
        raise HTTPException(status_code=404, detail="Instrumento no encontrado")
    
    return data

@router.get("/instruments/{symbol}/history")
def get_instrument_history(symbol: str, days: int = 30):
    historical_data = market_service.get_historical_data(symbol, days)
    if not historical_data:
        raise HTTPException(status_code=404, detail="Datos históricos no disponibles")
    
    return {"symbol": symbol, "history": historical_data}
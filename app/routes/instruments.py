# backend/app/routes/instruments.py
from fastapi import APIRouter

router = APIRouter(tags=["Instruments"])

@router.get("/instruments")
async def get_instruments():
    return {"message": "Lista de instrumentos"}
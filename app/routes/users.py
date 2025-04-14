# backend/app/routes/users.py
from fastapi import APIRouter

router = APIRouter(tags=["Users"])

@router.get("/users")
async def get_users():
    return {"message": "Lista de usuarios"}
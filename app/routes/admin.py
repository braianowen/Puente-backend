# backend/app/routes/admin.py
from fastapi import APIRouter, Depends
from requests import Session
from app.core.security import get_current_admin
from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse

router = APIRouter(tags=["Admin"])

@router.get("/admin/users", response_model=list[UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    return db.query(User).all()
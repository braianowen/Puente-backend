# # backend/app/routes/users.py
# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from app.db.database import get_db
# from app.models.user import User
# from app.schemas.user import UserResponse
# from app.core.security import get_current_admin  # Asegúrate de implementar esta función

# router = APIRouter(tags=["Users"])

# @router.get("/users", response_model=list[UserResponse])
# def get_users(
#     db: Session = Depends(get_db),
#     admin: User = Depends(get_current_admin)  # Solo administradores pueden acceder
# ):
#     users = db.query(User).all()
#     return users
# backend/main.py
from fastapi import FastAPI
from app.routes.auth import router as auth_router
from app.routes.users import router as users_router
from app.routes.instruments import router as instruments_router
from app.routes.favorites import router as favorites_router  
from app.routes.admin import router as admin_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(instruments_router)
app.include_router(favorites_router)
app.include_router(admin_router)

@app.get("/")
def root():
    return {"status": "API funcionando"}
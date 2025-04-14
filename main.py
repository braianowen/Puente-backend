# backend/main.py
from fastapi import FastAPI
from app.routes.auth import router as auth_router
from app.routes.users import router as users_router
from app.routes.instruments import router as instruments_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(instruments_router)

@app.get("/")
def root():
    return {"status": "API funcionando"}
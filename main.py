from fastapi import FastAPI
from app.routes.auth import router as auth_router
from app.routes.instruments import router as instruments_router
from app.routes.favorites import router as favorites_router  
from app.routes.admin import router as admin_router
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# Configuración CORS para Docker
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://frontend:80",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(instruments_router)
app.include_router(favorites_router)
app.include_router(admin_router)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/")
def root():
    return {"status": "API funcionando"}
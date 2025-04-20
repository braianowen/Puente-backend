# app/db/database.py
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:password@db:5432/mydb")

engine = create_engine(
    DATABASE_URL,
    connect_args={"options": f"-csearch_path={os.getenv('DB_SCHEMA', 'trading_schema')}"}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
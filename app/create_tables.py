from sqlalchemy import text
from app.db.database import Base, engine
from app.models.user import User  # Importa primero User
from app.models.favorite import Favorite  # Luego Favorite

def create_db():
    # Crear el esquema si no existe
    with engine.connect() as connection:
        connection.execute(text("CREATE SCHEMA IF NOT EXISTS trading_schema AUTHORIZATION admin;"))
        connection.commit()

    # Crear las tablas
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_db()
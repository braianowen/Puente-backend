import os
import time
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

def create_db():
    # Importar dentro de la función para evitar problemas de inicialización
    from app.db.database import Base, engine
    from app.models.user import User
    from app.models.favorite import Favorite
    
    max_retries = 5
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            # Crear el esquema si no existe
            with engine.connect() as connection:
                connection.execute(text(f"CREATE SCHEMA IF NOT EXISTS {os.getenv('DB_SCHEMA', 'trading_schema')} AUTHORIZATION admin;"))
                connection.commit()

            # Crear las tablas en el esquema correcto
            Base.metadata.create_all(bind=engine)
            print("Tablas creadas exitosamente")
            return
        except OperationalError as e:
            if attempt == max_retries - 1:
                raise
            print(f"Intento {attempt + 1} fallido. Reintentando en {retry_delay} segundos... Error: {str(e)}")
            time.sleep(retry_delay)

if __name__ == "__main__":
    create_db()
FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN echo '#!/bin/sh\n\
until PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -c "SELECT 1"; do\n\
  echo "PostgreSQL no está disponible - esperando..."\n\
  sleep 1\n\
done\n\
echo "PostgreSQL está listo"' > wait-for-postgres.sh && \
    chmod +x wait-for-postgres.sh

EXPOSE 8000

CMD ["sh", "-c", "./wait-for-postgres.sh && python create_tables.py && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]
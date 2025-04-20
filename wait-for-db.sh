#!/bin/sh

set -e

# Configuración desde variables de entorno
host=${DB_HOST:-db}
port=${DB_PORT:-5432}
user=${DB_USER:-admin}
password=${DB_PASSWORD:-password}
dbname=${DB_NAME:-mydb}

max_retries=30
retry_count=0

until PGPASSWORD=$password psql -h "$host" -p "$port" -U "$user" -d "$dbname" -c '\q' >/dev/null 2>&1 || [ $retry_count -eq $max_retries ]; do
  retry_count=$((retry_count+1))
  echo "Intento $retry_count/$max_retries - PostgreSQL no está disponible - esperando..."
  sleep 2
done

if [ $retry_count -eq $max_retries ]; then
  echo "PostgreSQL no está disponible después de $max_retries intentos - abortando"
  exit 1
fi

echo "PostgreSQL está listo - iniciando aplicación"
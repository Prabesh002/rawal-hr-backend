#!/bin/sh

set -e

echo "Waiting for the database to be ready at ${DB_HOST}:${DB_PORT}..."
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 2
done
echo "Database is ready!"

echo "Running database migrations..."
alembic upgrade head

echo "Seeding database with admin user if not exists..."
python app/scripts/seed.py

echo "Starting Gunicorn server..."
exec gunicorn -w "${WORKERS:-4}" -k uvicorn.workers.UvicornWorker app.main:app -b 0.0.0.0:8000

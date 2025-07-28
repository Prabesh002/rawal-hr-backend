#!/bin/sh

export PGPASSWORD="$DB_PASS"

echo "Waiting for the database to be ready..."

until pg_isready -h "$DB_HOST" -U "$DB_USER"; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 2
done

echo "Postgres is up - checking database existence..."

DB_EXISTS=$(psql -h "$DB_HOST" -U "$DB_USER" -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='${DB_NAME}'")

if [ "$DB_EXISTS" != "1" ]; then
  echo "Database '$DB_NAME' does not exist. Creating it..."
  createdb -h "$DB_HOST" -U "$DB_USER" "$DB_NAME"
  echo "Database '$DB_NAME' created!"
else
  echo "Database '$DB_NAME' already exists."
fi

echo "Running migrations..."
poetry run alembic upgrade head

echo "Starting Uvicorn server..."
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --reload-dir /app/app
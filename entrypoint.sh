#!/bin/sh

set -e

echo "Waiting for postgres..."
while ! nc -z db 5432; do
  sleep 0.5
done
echo "Postgres is up"

echo "Running migrations..."
alembic upgrade head

echo "Starting FastAPI..."
uvicorn app.main:app --host 0.0.0.0 --port 8000

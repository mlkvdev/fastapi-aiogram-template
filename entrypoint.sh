#!/bin/sh

until alembic upgrade head; do
  sleep 2
  echo "Retrying to apply migrations"
done
uvicorn backend.main:app --host 0.0.0.0 --port 8000
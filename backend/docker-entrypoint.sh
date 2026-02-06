#!/bin/bash
set -e

# Ждем пока база данных будет готова
echo "Waiting for database..."
for i in {1..30}; do
  if nc -z db 5432; then
    echo "Database is ready!"
    break
  fi
  echo "Waiting for database... ($i/30)"
  sleep 1
done

# Проверяем подключение еще раз
if ! nc -z db 5432; then
  echo "Database is not available after 30 seconds"
  exit 1
fi

# Применяем миграции
echo "Running migrations..."
cd /app
alembic upgrade head || echo "Migrations failed, continuing..."

# Запускаем приложение
exec "$@"


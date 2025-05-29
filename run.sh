#!/bin/bash
# подставляем переменные из окружения в подготовленный конфиг
set -e  # fail on error

echo "[run.sh] Checking required environment variables..."

: "${DATABASE_USER:?Missing DATABASE_USER}"
: "${DATABASE_PASSWORD:?Missing DATABASE_PASSWORD}"
: "${DATABASE_HOST:?Missing DATABASE_HOST}"
: "${DATABASE_NAME:?Missing DATABASE_NAME}"
cat config/koyeb-config.yaml | envsubst > config/config.yaml 
# необходимо для того, чтобы alembic смог найти наше приложение
export PYTHONPATH=.
# обновляем версию базы до последней
#alembic upgrade head 
echo "[run.sh] Running Alembic migrations..."
alembic upgrade head || { echo "Alembic migration failed"; exit 1; }
# запускаем сервер
python main.py
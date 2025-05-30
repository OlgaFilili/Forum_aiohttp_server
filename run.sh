#!/bin/bash
# подставляем переменные из окружения в подготовленный конфиг
set -e  # fail on error
if [ ! -f config/koyeb-config.yaml ]; then
  echo "❌ config/koyeb-config.yaml not found!"
  exit 1
fi
echo "[run.sh] Checking required environment variables..."
: "${POSTGRES_USER:?Missing DATABASE_USER}"

#cat config/koyeb-config.yaml | envsubst > config/config.yaml 
envsubst < config/koyeb-config.yaml > config/config.yaml
# необходимо для того, чтобы alembic смог найти наше приложение
export PYTHONPATH=.
# обновляем версию базы до последней
#alembic upgrade head 
echo "[run.sh] Running Alembic migrations..."
alembic upgrade head || { echo "Alembic migration failed"; exit 1; }
# запускаем сервер
python main.py
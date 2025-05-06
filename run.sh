# подставляем переменные из окружения в подготовленный конфиг
cat config/heroku_config.yaml | envsubst > config/config.yaml 
# необходимо для того, чтобы alembic смог найти наше приложение
export PYTHONPATH=. 
# обновляем версию базы до последней
alembic upgrade head 
# запускаем сервер
python main.py
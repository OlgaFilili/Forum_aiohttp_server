# Docker-команда FROM указывает базовый образ контейнера
# Наш базовый образ - это Linux с предустановленным python-3.7
FROM --platform=linux/amd64 ubuntu:jammy
FROM python:3.10.11
# gettext-base нужен для того, чтобы установить envsubst
RUN apt update && apt -y install gettext-base
# Скопируем файл с зависимостями в контейнер
COPY requirements.txt .
# Установим зависимости внутри контейнера
RUN pip install -r requirements.txt
# Скопируем остальные файлы в контейнер
COPY . .
# разрешаем наш скрипт на исполнение операционной системой
RUN chmod +x run.sh
# запускаем скрипт
CMD ["./run.sh"]
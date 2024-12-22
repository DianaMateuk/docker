FROM python:3.11-alpine

# Установка системных зависимостей
RUN apk add --no-cache --virtual .build-deps \
    gcc musl-dev mariadb-connector-c-dev

WORKDIR /docker_lab
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Удаление временных файлов
RUN apk del .build-deps

COPY . .
# Добавляем непривилегированного пользователя
RUN adduser -D appuser
USER appuser

EXPOSE 8000
CMD ["sh", "-c", "alembic upgrade head && uvicorn app:app --host 0.0.0.0 --port 8000"]

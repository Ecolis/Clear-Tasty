# Используем тот же базовый образ для консистентности
FROM python:3.12-slim

# Метаданные
LABEL maintainer="ваш-email@example.com"
LABEL version="1.0"
LABEL description="Микросервис погоды и сезонных рекомендаций"

# Рабочая директория
WORKDIR /app

# Копируем и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем код
COPY . .

# Открываем порт (другой, чтобы не было конфликтов)
EXPOSE 5002

# Команда запуска
CMD ["python", "app.py"]
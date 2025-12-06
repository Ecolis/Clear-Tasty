# Используем официальный легкий образ Python
FROM python:3.12-slim

# Устанавливаем метаданные (опционально)
LABEL maintainer="ваш-email@example.com"
LABEL version="1.0"
LABEL description="Микросервис статистики рецептов"

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл зависимостей в контейнер
COPY requirements.txt .

# Устанавливаем зависимости Python
# --no-cache-dir: не кэшируем, чтобы уменьшить размер образа
# --upgrade: обновляем pip до последней версии
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем весь код микросервиса в контейнер
COPY . .

# Открываем порт, на котором работает микросервис
EXPOSE 5001

# Команда для запуска приложения
# Используем python вместо flask run для простоты
CMD ["python", "app.py"]
# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем необходимые системные зависимости для работы с Tesseract и OpenCV
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей Python (requirements.txt)
COPY requirements.txt .

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта в контейнер
COPY . /app

# Открываем порт для Flask приложения
EXPOSE 5000

# Запускаем Flask приложение
CMD ["python", "app.py"]

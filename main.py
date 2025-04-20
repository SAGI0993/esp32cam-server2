from flask import Flask, request, jsonify
from PIL import Image
import easyocr
import cv2
import io
import numpy as np  # Добавлен импорт numpy
import os

app = Flask(__name__)

# Инициализируем EasyOCR
reader = easyocr.Reader(['en'], gpu=False)  # Можно изменить на ['en', 'ru'] для поддержки русского языка

@app.route("/")
def index():
    return "ESP32-CAM Flask Server is running!", 200

@app.route("/receive_image", methods=["POST"])
def receive_image():
    try:
        # Получаем "сырые" данные запроса
        raw_data = request.get_data()
        
        # Проверяем, есть ли вообще данные
        if not raw_data or len(raw_data) < 100:
            return jsonify({"error": "No image data received"}), 400

        # Преобразуем байты в изображение
        image = Image.open(io.BytesIO(raw_data))

        # Преобразуем изображение в OpenCV формат (для обработки)
        open_cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        # Преобразуем изображение в черно-белое для улучшения OCR
        gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)

        # Улучшаем изображение для OCR
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

        # Распознаем текст с изображения с помощью EasyOCR
        result = reader.readtext(thresh)

        # Извлекаем распознанный текст (если есть)
        text = ' '.join([r[1] for r in result]).strip().upper()

        # Сохраняем изображение с распознанным номером (опционально)
        filename = "received_with_plate.jpg"
        image.save(filename)

        return jsonify({
            "result": "Image received and saved!",
            "license_plate": text  # Возвращаем распознанный номер
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render использует переменную PORT
    app.run(host="0.0.0.0", port=port)

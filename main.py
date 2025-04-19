from flask import Flask, request
import numpy as np
import cv2
import pytesseract

app = Flask(__name__)

# Страница по умолчанию
@app.route("/")
def home():
    return "ESP32-CAM Parking Server"

# Обработка POST-запроса с изображением
@app.route("/upload_image", methods=["POST"])
def upload_image():
    try:
        # Получаем изображение в виде байтов
        image = request.data
        nparr = np.frombuffer(image, np.uint8)

        # Преобразуем в изображение OpenCV
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            return "INVALID_IMAGE", 400

        # Распознавание текста
        text = pytesseract.image_to_string(img).upper()
        print("Распознанный текст:", text)

        # Поиск известных номеров
        known_plates = ["SAG", "MED", "ARU", "XAN", "ADMIN"]
        for plate in known_plates:
            if plate in text:
                return plate, 200

        return "UNKNOWN", 200
    except Exception as e:
        print("Ошибка при обработке:", e)
        return "ERROR", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

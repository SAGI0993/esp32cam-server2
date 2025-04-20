from flask import Flask, request, jsonify
from PIL import Image
import pytesseract
import cv2
import io
import os

app = Flask(__name__)

# Настройка пути к Tesseract (если необходимо для pytesseract)
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'  # Убедись, что tesseract установлен

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

        # Улучшаем изображение для Tesseract
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

        # Распознаем текст с изображения
        text = pytesseract.image_to_string(thresh, config='--psm 8').strip().upper()

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

from flask import Flask, request, jsonify
import easyocr
from PIL import Image
import numpy as np
import io

app = Flask(__name__)

# Инициализируем EasyOCR
reader = easyocr.Reader(['en'], gpu=False)  # Можно добавить другие языки

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

        # Преобразуем изображение в формат numpy для обработки
        open_cv_image = np.array(image)

        # Преобразуем изображение в черно-белое для улучшения качества
        gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)

        # Распознаем текст с изображения с помощью EasyOCR
        result = reader.readtext(gray)

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
    app.run(host="0.0.0.0", port=10000)

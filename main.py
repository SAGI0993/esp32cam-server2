from flask import Flask, request, jsonify
from PIL import Image
import io
import os

app = Flask(__name__)

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
        
        # Сохраняем файл с уникальным именем (по желанию можно просто "received.jpg")
        save_path = "received.jpg"
        image.save(save_path)

        return jsonify({"result": "Image received and saved!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render использует переменную PORT
    app.run(host="0.0.0.0", port=port)

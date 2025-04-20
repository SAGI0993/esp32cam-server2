from flask import Flask, request, jsonify
from PIL import Image
import cv2
import numpy as np
import os
import io

app = Flask(__name__)

# Загружаем шаблоны символов из папки templates
TEMPLATE_FOLDER = "templates"
templates = {}

for filename in os.listdir(TEMPLATE_FOLDER):
    if filename.endswith(".png"):
        label = filename.split(".")[0].upper()
        img_path = os.path.join(TEMPLATE_FOLDER, filename)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        _, img_bin = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        templates[label] = img_bin

@app.route("/")
def index():
    return "🚀 ESP32-CAM Template Matching Server is running!"

@app.route("/receive_image", methods=["POST"])
def receive_image():
    try:
        raw_data = request.get_data()

        if not raw_data or len(raw_data) < 100:
            return jsonify({"error": "No image data received"}), 400

        image = Image.open(io.BytesIO(raw_data))
        img_bgr = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

        # Поиск контуров символов
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[0])  # Сортировка слева направо

        result_text = ""

        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if w < 10 or h < 10:
                continue  # отсекаем шум

            roi = binary[y:y+h, x:x+w]
            roi_resized = cv2.resize(roi, (20, 20))  # унификация размера

            best_match = "?"
            best_score = 0

            for label, tmpl in templates.items():
                tmpl_resized = cv2.resize(tmpl, (20, 20))
                match_score = np.sum(roi_resized == tmpl_resized)
                if match_score > best_score:
                    best_score = match_score
                    best_match = label

            result_text += best_match

        image.save("last_received.jpg")  # на случай отладки

        return jsonify({
            "result": "Image received",
            "license_plate": result_text
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

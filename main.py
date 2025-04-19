from flask import Flask, request, jsonify
import cv2
import numpy as np
import pytesseract
from io import BytesIO

app = Flask(__name__)

# Настройка пути к Tesseract (если необходимо для pytesseract)
# Убедись, что Tesseract установлен на твоем сервере.
# На Windows, например, путь может быть: "C:/Program Files/Tesseract-OCR/tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

@app.route('/receive_image', methods=['POST'])
def receive_image():
    try:
        # Получаем изображение из запроса
        file = request.files['image']
        img_bytes = file.read()

        # Преобразуем байты в изображение
        np_arr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # Преобразуем изображение в черно-белое для улучшения OCR
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Используем pytesseract для распознавания текста на изображении
        text = pytesseract.image_to_string(gray, config='--psm 6')

        # Обрабатываем полученный текст
        text = text.strip().upper()  # Убираем пробелы и делаем текст верхним регистром

        print(f"Распознанный номер: {text}")

        # Отправляем распознанный номер обратно на ESP32
        return jsonify({'plate': text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

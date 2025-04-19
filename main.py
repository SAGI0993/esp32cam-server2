from flask import Flask, request, render_template
import numpy as np
import cv2

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_image', methods=['POST'])
def upload_image():
    try:
        image = request.data
        print(f"[INFO] Получено изображение, размер: {len(image)} байт")

        nparr = np.frombuffer(image, np.uint8)
        print("[INFO] Преобразовано в numpy array")

        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            print("[ERROR] OpenCV не смог декодировать изображение")
            return "Ошибка декодирования изображения", 500

        print(f"[INFO] Изображение успешно декодировано, размер: {img.shape}")

        # Сохраняем для отладки
        cv2.imwrite("received.jpg", img)
        print("[INFO] Изображение сохранено как received.jpg")

        # Здесь можно вставить обработку (распознавание и т.д.)
        return "OK"

    except Exception as e:
        print(f"[EXCEPTION] Произошла ошибка: {e}")
        return "ERROR", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

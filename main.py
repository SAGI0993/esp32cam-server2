
from flask import Flask, request, jsonify
import base64

app = Flask(__name__)

@app.route('/recognize', methods=['POST'])
def recognize():
    data = request.get_json()
    if not data or 'image' not in data:
        return jsonify({'error': 'No image provided'}), 400

    # Здесь могла бы быть обработка изображения
    # Но мы просто вернём "MED" как тест
    return jsonify({'plate': 'MED'})

@app.route('/')
def home():
    return 'ESP32-CAM API is running'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

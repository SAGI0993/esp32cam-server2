from flask import Flask, request
import cv2
import numpy as np
import pytesseract

app = Flask(__name__)

@app.route("/upload_image", methods=["POST"])
def upload_image():
    image = request.data
    nparr = np.frombuffer(image, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    text = pytesseract.image_to_string(img)
    print("Распознанный текст:", text)

    # Фильтруем, оставляя только номера, например, "SAG"
    known_plates = ["SAG", "MED", "ARU", "XAN", "ADMIN"]
    for plate in known_plates:
        if plate in text:
            return plate
    return "UNKNOWN"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

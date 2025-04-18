# main.py (сервер)
from flask import Flask, request, jsonify

app = Flask(__name__)

ALLOWED_PLATES = ["MED", "ARU", "SAG", "XAN"]
ADMIN_PLATE = "ADMIN"
cars_in = 0
max_cars = 5

@app.route("/check_plate", methods=["POST"])
def check_plate():
    global cars_in
    plate = request.json.get("plate", "").upper()

    if plate in ALLOWED_PLATES and cars_in < max_cars:
        cars_in += 1
        return jsonify({"access": True})
    elif plate == ADMIN_PLATE:
        return jsonify({"access": True})
    return jsonify({"access": False})

@app.route("/")
def index():
    return "ESP32-CAM Parking Server"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

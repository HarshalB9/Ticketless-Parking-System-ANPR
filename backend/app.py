from flask import Flask, request, jsonify
from flask_cors import CORS
from inference.detect_plate import detect_plate
from inference.ocr import get_plate_number
from db.mongo import insert_entry, find_and_remove_vehicle
from db.mongo import collection  

app = Flask(__name__)
CORS(app)
# CORS(app, resources={r"/api/*": {"origins": "*"}})
# CORS(app, origins=[" http://127.0.0.1:5000"], supports_credentials=True)

@app.route("/api/entry", methods=["POST"])
def vehicle_entry():
    image = request.files["image"]
    image_path = "temp_entry.jpg"
    image.save(image_path)

    detect_plate(image_path)  # YOLO + crop
    plate_number = get_plate_number("plate.jpg")  # OCR

    entry = insert_entry(plate_number)
    return jsonify({
        "vehicle_number": entry["vehicle_number"],
        "in_time": entry["in_time"]
    })



@app.route("/api/exit", methods=["POST"])
def vehicle_exit():
    image = request.files["image"]
    image_path = "temp_exit.jpg"
    image.save(image_path)

    detect_plate(image_path)
    plate_number = get_plate_number("plate.jpg")

    response = find_and_remove_vehicle(plate_number)
    return jsonify(response)


@app.route('/api/vehicles-in-parking', methods=['GET'])
def get_vehicles_in_parking():
    vehicles = collection.find({"out_time": {"$exists": False}})
    result = []
    for vehicle in vehicles:
        result.append({
            "_id": str(vehicle["_id"]),
            "vehicleNumber": vehicle.get("vehicle_number", "N/A"),
            "ownerName": vehicle.get("owner_name", "Unknown"),  # update if you have this
            "timeIn": vehicle["in_time"],
            "timeOut": None,
            "paymentStatus": "Pending"
        })
    return jsonify(result)

@app.route('/api/vehicle-count', methods=['GET'])
def vehicle_count():
    try:
        count = collection.count_documents({})  # Only count vehicles still inside
        return jsonify({"count": count})
    except Exception as e:
        print("Error fetching vehicle count:", e)
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    app.run(debug=True)

# from pymongo import MongoClient
# from datetime import datetime

# MONGO_URI = "mongodb+srv://harshalbhusare8750:sI35uSV3OXVk2xqK@anprdatabase.9e8npny.mongodb.net/anpr_database?retryWrites=true&w=majority"
# client = MongoClient(MONGO_URI)
# db = client["anpr_database"]
# collection = db["plate_numbers"]

# # def insert_entry(plate_number):
# #     doc = {
# #         "plate_number": plate_number,
# #         "entry_time": datetime.now()
# #     }
# #     return collection.insert_one(doc).inserted_id
# from datetime import datetime
# from bson.objectid import ObjectId

# def insert_entry(plate_number):
#     entry = {
#         "vehicle_number": plate_number,
#         "in_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     }
#     result = collection.insert_one(entry)
#     entry["_id"] = result.inserted_id
#     return entry

# def find_and_remove_vehicle(plate_number):
#     doc = collection.find_one({"plate_number": plate_number})
#     if not doc:
#         return {"status": "not_found"}

#     entry_time = doc["entry_time"]
#     current_time = datetime.now()
#     duration_minutes = (current_time - entry_time).total_seconds() / 60
#     charge_units = int(duration_minutes // 30) + (1 if duration_minutes % 30 > 0 else 0)
#     total_charge = charge_units * 5

#     collection.delete_one({"_id": doc["_id"]})

#     return {
#         "vehicle_number": plate_number,
#         "in_time": entry_time.strftime("%Y-%m-%d %H:%M:%S"),
#         "out_time": current_time.strftime("%Y-%m-%d %H:%M:%S"),
#         "duration_minutes": round(duration_minutes, 2),
#         "charge": total_charge
#     }

from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId

MONGO_URI = "mongodb+srv://harshalbhusare8750:sI35uSV3OXVk2xqK@anprdatabase.9e8npny.mongodb.net/anpr_database?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client["anpr_database"]
collection = db["plate_numbers"]

def insert_entry(plate_number):
    entry = {
        "vehicle_number": plate_number,
        "in_time": datetime.now()
    }
    result = collection.insert_one(entry)
    entry["_id"] = result.inserted_id
    return entry

def find_and_remove_vehicle(plate_number):
    doc = collection.find_one({"vehicle_number": plate_number})
    if not doc:
        return {"status": "not_found"}

    in_time = doc["in_time"]
    out_time = datetime.now()
    duration_minutes = (out_time - in_time).total_seconds() / 60

    charge_units = int(duration_minutes // 30) + (1 if duration_minutes % 30 > 0 else 0)
    total_charge = charge_units * 5

    collection.delete_one({"_id": doc["_id"]})

    return {
        "vehicle_number": plate_number,
        "in_time": in_time.strftime("%Y-%m-%d %H:%M:%S"),
        "out_time": out_time.strftime("%Y-%m-%d %H:%M:%S"),
        "duration_minutes": round(duration_minutes, 2),
        "charge": total_charge
    }


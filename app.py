from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

db = client["student_db"]

students = db["students"]

@app.route("/")
def home():
    return "Welcome to Student API (MongoDB)"


#POST API
@app.route("/students", methods=["POST"])
def add_student():

    data = request.get_json()

    student = {
        "name": data["name"],
        "age": data["age"],
        "course": data["course"]
    }

    result = students.insert_one(student)

    return jsonify({
        "message": "Student added successfully",
        "id": str(result.inserted_id)
    }), 201

#GET API
@app.route("/students", methods=["GET"])
def get_students():

    data = []

    for student in students.find():

        data.append({
            "id": str(student["_id"]),
            "name": student["name"],
            "age": student["age"],
            "course": student["course"]
        })

    return jsonify(data)



# UPDATE API
@app.route("/students/<id>", methods=["PUT"])
def update_student(id):

    data = request.get_json()

    result = students.update_one(
        {"_id": ObjectId(id)},
        {
            "$set": {
                "name": data["name"],
                "age": data["age"],
                "course": data["course"]
            }
        }
    )

    if result.matched_count == 0:
        return jsonify({"message": "Student not found"}), 404

    return jsonify({"message": "Student updated successfully"})

# DELETE API
@app.route("/students/<id>", methods=["DELETE"])
def delete_student(id):

    result = students.delete_one(
        {"_id": ObjectId(id)}
    )

    if result.deleted_count == 0:
        return jsonify({"message": "Student not found"}), 404

    return jsonify({"message": "Student deleted successfully"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

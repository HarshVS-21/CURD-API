from flask import Flask, request, jsonify 
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app and configure database
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///students.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Creating Flask app
db = SQLAlchemy(app)
#Modelling the table
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    course = db.Column(db.String(100), nullable=False)


#POST API
@app.route("/students", methods=["POST"])
def add_student():
    data = request.get_json()

    student = Student(
        name=data["name"],
        age=data["age"],
        course=data["course"]
    )

    db.session.add(student)
    db.session.commit()

    return jsonify({"message": "Student added successfully"}), 201


#GET API
@app.route("/students", methods=["GET"])
def get_students():
    students = Student.query.all()

    result = []

    for student in students:
        result.append({
            "id": student.id,
            "name": student.name,
            "age": student.age,
            "course": student.course
        })

    return jsonify(result), 200
# UPDATE API
@app.route("/students/<int:id>", methods=["PUT"])
def update_student(id):
    student = Student.query.get_or_404(id)

    data = request.get_json()

    if "name" in data:
        student.name = data["name"]

    if "age" in data:
        student.age = data["age"]

    if "course" in data:
        student.course = data["course"]

    db.session.commit()

    return jsonify({"message": "Student updated successfully"})


# DELETE API
@app.route("/students/<int:id>", methods=["DELETE"])
def delete_student(id):
    student = Student.query.get_or_404(id)

    db.session.delete(student)
    db.session.commit()

    return jsonify({"message": "Student deleted successfully"})
    

#  Main Page
@app.route("/")
def home():
    return "Welcome to Student API"


# Create Database
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
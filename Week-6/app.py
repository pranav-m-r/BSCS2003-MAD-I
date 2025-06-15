import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource

app = Flask(__name__)

# Get the absolute path of the current directory
basedir = os.path.abspath(os.path.dirname(__file__))

# Configure the SQLite database URI
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///api_database.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
api = Api(app)


# Database Models
class Course(db.Model):
    __tablename__ = "course"
    course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_name = db.Column(db.String, nullable=False)
    course_code = db.Column(db.String, unique=True, nullable=False)
    course_description = db.Column(db.String)


class Student(db.Model):
    __tablename__ = "student"
    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    roll_number = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String)


class Enrollment(db.Model):
    __tablename__ = "enrollment"
    enrollment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(
        db.Integer, db.ForeignKey("student.student_id"), nullable=False
    )
    course_id = db.Column(db.Integer, db.ForeignKey("course.course_id"), nullable=False)


# RESTful Resources
class CourseAPI(Resource):
    def get(self, course_id):
        if course_id:
            course = db.session.query(Course).get(course_id)
            if course:
                return {
                    "course_id": course.course_id,
                    "course_name": course.course_name,
                    "course_code": course.course_code,
                    "course_description": course.course_description,
                }, 200
            return {"message": "Course not found"}, 404

    def post(self):
        data = request.get_json()
        if not data.get("course_name"):
            return {
                "error_code": "COURSE001",
                "error_message": "Course Name is required",
            }, 400
        if not data.get("course_code"):
            return {
                "error_code": "COURSE002",
                "error_message": "Course Code is required",
            }, 400
        if (
            db.session.query(Course)
            .filter(Course.course_code == data["course_code"])
            .first()
        ):
            return {}, 409
        new_course = Course(
            course_name=data["course_name"],
            course_code=data["course_code"],
            course_description=data.get("course_description"),
        )
        db.session.add(new_course)
        db.session.commit()
        return {
            "course_id": new_course.course_id,
            "course_name": new_course.course_name,
            "course_code": new_course.course_code,
            "course_description": new_course.course_description,
        }, 201

    def put(self, course_id):
        course = db.session.query(Course).get(course_id)
        if not course:
            return {"message": "Course not found"}, 404
        data = request.get_json()
        course.course_name = data.get("course_name", course.course_name)
        course.course_code = data.get("course_code", course.course_code)
        course.course_description = data.get(
            "course_description", course.course_description
        )
        db.session.commit()
        return {
            "course_id": course.course_id,
            "course_name": course.course_name,
            "course_code": course.course_code,
            "course_description": course.course_description,
        }, 200

    def delete(self, course_id):
        course = db.session.query(Course).get(course_id)
        if not course:
            return {"message": "Course not found"}, 404
        db.session.delete(course)
        db.session.commit()
        return {"message": "Successfully deleted"}, 200


class StudentAPI(Resource):
    def get(self, student_id):
        if student_id:
            student = db.session.query(Student).get(student_id)
            if student:
                return {
                    "student_id": student.student_id,
                    "first_name": student.first_name,
                    "last_name": student.last_name,
                    "roll_number": student.roll_number,
                }, 200
            return {"message": "Student not found"}, 404

    def post(self):
        data = request.get_json()
        if not data.get("roll_number"):
            return {
                "error_code": "STUDENT001",
                "error_message": "Roll Number required",
            }, 400
        if not data.get("first_name"):
            return {
                "error_code": "STUDENT002",
                "error_message": "First Name is required",
            }, 400
        if (
            db.session.query(Student)
            .filter(Student.roll_number == data["roll_number"])
            .first()
        ):
            return {}, 409
        new_student = Student(
            roll_number=data["roll_number"],
            first_name=data["first_name"],
            last_name=data.get("last_name"),
        )
        db.session.add(new_student)
        db.session.commit()
        return {
            "student_id": new_student.student_id,
            "first_name": new_student.first_name,
            "last_name": new_student.last_name,
            "roll_number": new_student.roll_number,
        }, 201

    def put(self, student_id):
        student = db.session.query(Student).get(student_id)
        if not student:
            return {"message": "Student not found"}, 404
        data = request.get_json()
        student.first_name = data.get("first_name", student.first_name)
        student.last_name = data.get("last_name", student.last_name)
        student.roll_number = data.get("roll_number", student.roll_number)
        db.session.commit()
        return {
            "student_id": student.student_id,
            "first_name": student.first_name,
            "last_name": student.last_name,
            "roll_number": student.roll_number,
        }, 200

    def delete(self, student_id):
        student = db.session.query(Student).get(student_id)
        if not student:
            return {"message": "Student not found"}, 404
        db.session.delete(student)
        db.session.commit()
        return {"message": "Successfully deleted"}, 200


class EnrollmentAPI(Resource):
    def get(self, student_id):
        enrollments = (
            db.session.query(Enrollment)
            .filter(
                Enrollment.student_id == student_id,
            )
            .all()
        )
        if enrollments:
            return [
                {
                    "enrollment_id": enrollment.enrollment_id,
                    "student_id": enrollment.student_id,
                    "course_id": enrollment.course_id,
                }
                for enrollment in enrollments
            ], 200
        return {"message": "Enrollment not found"}, 404

    def post(self, student_id):
        data = request.get_json()
        student = db.session.query(Student).get(student_id)
        if not student:
            return {
                "error_code": "ENROLLMENT002",
                "error_message": "Student does not exist",
            }, 404
        course = db.session.query(Course).get(data["course_id"])
        if not course:
            return {
                "error_code": "ENROLLMENT001",
                "error_message": "Course does not exist",
            }, 404
        new_enrollment = Enrollment(student_id=student_id, course_id=data["course_id"])
        db.session.add(new_enrollment)
        db.session.commit()
        return [
            {
                "enrollment_id": new_enrollment.enrollment_id,
                "student_id": new_enrollment.student_id,
                "course_id": new_enrollment.course_id,
            }
        ], 201

    def delete(self, student_id, course_id):
        enrollment = (
            db.session.query(Enrollment)
            .filter(
                Enrollment.student_id == student_id, Enrollment.course_id == course_id
            )
            .first()
        )
        if not enrollment:
            return {"message": "Enrollment not found"}, 404
        db.session.delete(enrollment)
        db.session.commit()
        return {"message": "Successfully deleted"}, 200


# Add Resources to API
api.add_resource(CourseAPI, "/api/course", "/api/course/<int:course_id>")
api.add_resource(StudentAPI, "/api/student", "/api/student/<int:student_id>")
api.add_resource(
    EnrollmentAPI,
    "/api/student/<int:student_id>/course",
    "/api/student/<int:student_id>/course/<int:course_id>",
)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

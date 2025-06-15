from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///week7_database.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
api = Api(app)

# Database Models
class Student(db.Model):
    __tablename__ = "student"
    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    roll_number = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String)

class Course(db.Model):
    __tablename__ = "course"
    course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_code = db.Column(db.String, unique=True, nullable=False)
    course_name = db.Column(db.String, nullable=False)
    course_description = db.Column(db.String)

class Enrollment(db.Model):
    __tablename__ = "enrollments"
    enrollment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    estudent_id = db.Column(db.Integer, db.ForeignKey("student.student_id"), nullable=False)
    ecourse_id = db.Column(db.Integer, db.ForeignKey("course.course_id"), nullable=False)
    student = db.relationship("Student", backref=db.backref("enrollments", cascade="all, delete-orphan"))
    course = db.relationship("Course", backref=db.backref("enrollments", cascade="all, delete-orphan"))

# RESTful Resources for Update and Delete
class StudentUpdateAPI(Resource):
    def post(self, student_id):
        student = Student.query.get_or_404(student_id)
        data = request.form
        student.first_name = data["f_name"]
        student.last_name = data["l_name"]
        
        # Update enrollments
        Enrollment.query.filter_by(estudent_id=student_id).delete()
        for course_id in data.getlist("courses"):
            enrollment = Enrollment(estudent_id=student.student_id, ecourse_id=int(course_id))
            db.session.add(enrollment)

        db.session.commit()
        return {"message": "Student updated successfully"}, 200

class StudentDeleteAPI(Resource):
    def get(self, student_id):
        student = Student.query.get_or_404(student_id)
        db.session.delete(student)
        db.session.commit()
        return {"message": "Student deleted successfully"}, 200

class CourseUpdateAPI(Resource):
    def post(self, course_id):
        course = Course.query.get_or_404(course_id)
        data = request.form
        course.course_name = data["c_name"]
        course.course_description = data["desc"]
        db.session.commit()
        return {"message": "Course updated successfully"}, 200

class CourseDeleteAPI(Resource):
    def get(self, course_id):
        course = Course.query.get_or_404(course_id)
        db.session.delete(course)
        db.session.commit()
        return {"message": "Course deleted successfully"}, 200

# Add Resources to API
api.add_resource(StudentUpdateAPI, "/student/<int:student_id>/update")
api.add_resource(StudentDeleteAPI, "/student/<int:student_id>/delete")
api.add_resource(CourseUpdateAPI, "/course/<int:course_id>/update")
api.add_resource(CourseDeleteAPI, "/course/<int:course_id>/delete")

# Routes for HTML pages
@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students), 200

@app.route('/student/create', methods=['GET', 'POST'])
def create_student():
    if request.method == 'POST':
        roll = request.form['roll']
        first_name = request.form['f_name']
        last_name = request.form['l_name']
        
        if Student.query.filter_by(roll_number=roll).first():
            return render_template('error.html', message="Roll number already exists."), 409
        
        student = Student(roll_number=roll, first_name=first_name, last_name=last_name)
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('index')), 200
    return render_template('add_student.html'), 200

@app.route('/student/<int:student_id>')
def student_detail(student_id):
    student = Student.query.get_or_404(student_id)
    enrollments = Enrollment.query.filter_by(estudent_id=student_id).all()
    return render_template('student_details.html', student=student, enrollments=enrollments), 200

@app.route('/student/<int:student_id>/withdraw/<int:course_id>')
def withdraw_course(student_id, course_id):
    enrollment = Enrollment.query.filter_by(estudent_id=student_id, ecourse_id=course_id).first()
    if enrollment:
        db.session.delete(enrollment)
        db.session.commit()
    return redirect(url_for('student_detail', student_id=student_id)), 200

@app.route('/courses')
def courses():
    courses = Course.query.all()
    return render_template('courses.html', courses=courses), 200

@app.route('/course/create', methods=['GET', 'POST'])
def create_course():
    if request.method == 'POST':
        code = request.form['code']
        name = request.form['c_name']
        desc = request.form['desc']
        
        if Course.query.filter_by(course_code=code).first():
            return render_template('error.html', message="Course code already exists."), 409
        
        course = Course(course_code=code, course_name=name, course_description=desc)
        db.session.add(course)
        db.session.commit()
        return redirect(url_for('courses')), 200
    return render_template('add_course.html'), 200

@app.route('/course/<int:course_id>')
def course_detail(course_id):
    course = Course.query.get_or_404(course_id)
    enrollments = Enrollment.query.filter_by(ecourse_id=course_id).all()
    return render_template('course_details.html', course=course, enrollments=enrollments), 200

@app.route('/course/<int:course_id>/update', methods=['GET', 'POST'])
def update_course(course_id):
    course = Course.query.get_or_404(course_id)
    if request.method == 'POST':
        course.course_name = request.form['c_name']
        course.course_description = request.form['desc']
        db.session.commit()
        return redirect(url_for('courses')), 200
    return render_template('update_course.html', course=course), 200

@app.route('/student/<int:student_id>/update', methods=['GET', 'POST'])
def update_student(student_id):
    student = Student.query.get_or_404(student_id)
    if request.method == 'POST':
        student.first_name = request.form['f_name']
        student.last_name = request.form['l_name']
        
        # Update enrollments
        Enrollment.query.filter_by(estudent_id=student_id).delete()
        selected_courses = request.form.getlist('courses')
        
        for course_id in selected_courses:
            enrollment = Enrollment(estudent_id=student.student_id, ecourse_id=int(course_id))
            db.session.add(enrollment)

        db.session.commit()
        return redirect(url_for('index')), 200
    else:
        courses = Course.query.all()
        enrolled_courses = [e.ecourse_id for e in Enrollment.query.filter_by(estudent_id=student_id).all()]
        return render_template('update_student.html', student=student, courses=courses, enrolled_courses=enrolled_courses), 200

if __name__ == '__main__':
    app.run(debug=True)
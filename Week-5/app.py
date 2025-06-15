from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define models
class Student(db.Model):
    __tablename__ = 'student'
    student_id = db.Column(db.Integer, primary_key=True)
    roll_number = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String)

class Course(db.Model):
    __tablename__ = 'course'
    course_id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String, unique=True, nullable=False)
    course_name = db.Column(db.String, nullable=False)
    course_description = db.Column(db.String)

class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    enrollment_id = db.Column(db.Integer, primary_key=True)
    estudent_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    ecourse_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), nullable=False)

# Define routes
@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

@app.route('/student/create', methods=['GET', 'POST'])
def create_student():
    if request.method == 'POST':
        roll = request.form['roll']
        first_name = request.form['f_name']
        last_name = request.form['l_name']
        courses_selected = request.form.getlist('courses')
        
        # Check for duplicate roll number
        if Student.query.filter_by(roll_number=roll).first():
            return render_template('error.html', message="Roll number already exists.")

        # Add student to database
        student = Student(roll_number=roll, first_name=first_name, last_name=last_name)
        db.session.add(student)
        db.session.flush()  # Flush to get student ID without committing

        # Add enrollments
        for course_id in courses_selected:
            enrollment = Enrollment(estudent_id=student.student_id, ecourse_id=int(course_id))
            db.session.add(enrollment)
        
        db.session.commit()
        return redirect(url_for('index'))
    else:
        courses = Course.query.all()
        return render_template('add_student.html', courses=courses)

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
        return redirect(url_for('index'))
    else:
        courses = Course.query.all()
        enrolled_courses = [e.ecourse_id for e in Enrollment.query.filter_by(estudent_id=student_id).all()]
        return render_template('update_student.html', student=student, courses=courses, enrolled_courses=enrolled_courses)

@app.route('/student/<int:student_id>/delete')
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    Enrollment.query.filter_by(estudent_id=student_id).delete()
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/student/<int:student_id>')
def student_details(student_id):
    student = Student.query.get_or_404(student_id)
    enrollments = Enrollment.query.filter_by(estudent_id=student_id).all()
    courses = [Course.query.get(e.ecourse_id) for e in enrollments]
    return render_template('student_details.html', student=student, courses=courses)

# Run the application
if __name__ == '__main__':
    app.run(debug=True)

from app import app, db, Student, Course, Enrollment

def initialize_database():
    with app.app_context():
        # Drop all tables and create them fresh
        db.drop_all()
        db.create_all()

        # Insert predefined courses
        courses = [
            Course(course_code="CSE01", course_name="MAD I", course_description="Modern Application Development - I"),
            Course(course_code="CSE02", course_name="DBMS", course_description="Database Management Systems"),
            Course(course_code="CSE03", course_name="PDSA", course_description="Programming, Data Structures, and Algorithms using Python"),
            Course(course_code="BST13", course_name="BDM", course_description="Business Data Management")
        ]
        db.session.bulk_save_objects(courses)
        db.session.commit()

        # Insert sample students
        students = [
            Student(roll_number="21BCS001", first_name="Alice", last_name="Smith"),
            Student(roll_number="21BCS002", first_name="Bob", last_name="Johnson"),
            Student(roll_number="21BCS003", first_name="Charlie", last_name="Brown")
        ]
        db.session.bulk_save_objects(students)
        db.session.commit()  # Commit to assign IDs to students

        # Fetch the course IDs to use in enrollments
        course1 = Course.query.filter_by(course_code="CSE01").first()
        course2 = Course.query.filter_by(course_code="CSE02").first()
        course3 = Course.query.filter_by(course_code="CSE03").first()
        course4 = Course.query.filter_by(course_code="BST13").first()

        # Fetch the student IDs and create enrollments
        student1 = Student.query.filter_by(roll_number="21BCS001").first()
        student2 = Student.query.filter_by(roll_number="21BCS002").first()
        student3 = Student.query.filter_by(roll_number="21BCS003").first()

        enrollments = [
            Enrollment(estudent_id=student1.student_id, ecourse_id=course1.course_id),
            Enrollment(estudent_id=student1.student_id, ecourse_id=course2.course_id),
            Enrollment(estudent_id=student2.student_id, ecourse_id=course2.course_id),
            Enrollment(estudent_id=student2.student_id, ecourse_id=course3.course_id),
            Enrollment(estudent_id=student3.student_id, ecourse_id=course1.course_id),
            Enrollment(estudent_id=student3.student_id, ecourse_id=course4.course_id)
        ]

        db.session.bulk_save_objects(enrollments)
        db.session.commit()

        print("Database initialized with sample data.")

if __name__ == "__main__":
    initialize_database()

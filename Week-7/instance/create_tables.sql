-- Create the Course table
CREATE TABLE course (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_name TEXT NOT NULL,
    course_code TEXT UNIQUE NOT NULL,
    course_description TEXT
);

-- Create the Student table
CREATE TABLE student (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    roll_number TEXT UNIQUE NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT
);

-- Create the Enrollment table
CREATE TABLE enrollments (
    enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    estudent_id INTEGER NOT NULL,
    ecourse_id INTEGER NOT NULL,
    FOREIGN KEY (estudent_id) REFERENCES student(student_id),
    FOREIGN KEY (ecourse_id) REFERENCES course(course_id)
);

-- Insert sample data into the Course table
INSERT INTO course (course_name, course_code, course_description) VALUES
('Mathematics', 'MATH101', 'Basic Mathematics course'),
('Physics', 'PHYS101', 'Introduction to Physics'),
('Chemistry', 'CHEM101', 'Basic Chemistry course'),
('Biology', 'BIOL101', 'Introduction to Biology');

-- Insert sample data into the Student table
INSERT INTO student (roll_number, first_name, last_name) VALUES
('1001', 'John', 'Doe'),
('1002', 'Jane', 'Smith'),
('1003', 'Alice', 'Johnson'),
('1004', 'Bob', 'Brown');

-- Insert sample data into the Enrollment table
INSERT INTO enrollments (estudent_id, ecourse_id) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4);
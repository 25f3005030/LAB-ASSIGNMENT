import sqlite3
import os

# Ensure instance folder exists
os.makedirs('instance', exist_ok=True)

# Connect to database inside instance folder
conn = sqlite3.connect('instance/database.sqlite3')
cursor = conn.cursor()

# Create student table
cursor.execute('''
CREATE TABLE IF NOT EXISTS student (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    roll_number TEXT UNIQUE NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT
)
''')

# Create course table
cursor.execute('''
CREATE TABLE IF NOT EXISTS course (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_code TEXT UNIQUE NOT NULL,
    course_name TEXT NOT NULL,
    course_description TEXT
)
''')

# Create enrollments table
cursor.execute('''
CREATE TABLE IF NOT EXISTS enrollments (
    enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    estudent_id INTEGER NOT NULL,
    ecourse_id INTEGER NOT NULL,
    FOREIGN KEY (estudent_id) REFERENCES student(student_id),
    FOREIGN KEY (ecourse_id) REFERENCES course(course_id)
)
''')

# Insert pre-loaded courses
courses_data = [
    (1, 'CSE01', 'MAD I', 'Modern Application Development - I'),
    (2, 'CSE02', 'DBMS', 'Database management Systems'),
    (3, 'CSE03', 'PDSA', 'Programming, Data Structures and Algorithms using Python'),
    (4, 'BST13', 'BDM', 'Business Data Management')
]

cursor.executemany('''
INSERT OR IGNORE INTO course (course_id, course_code, course_name, course_description)
VALUES (?, ?, ?, ?)
''', courses_data)

conn.commit()
conn.close()

print("Database tables created successfully inside instance folder! 🎉")
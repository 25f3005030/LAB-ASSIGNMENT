from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3' 
db = SQLAlchemy(app)

# Database Models
class Student(db.Model):
    __tablename__ = 'student'
    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    roll_number = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String)
    enrollments = db.relationship('Enrollment', backref='student', cascade='all, delete-orphan')

class Course(db.Model):
    __tablename__ = 'course'
    course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_code = db.Column(db.String, unique=True, nullable=False)
    course_name = db.Column(db.String, nullable=False)
    course_description = db.Column(db.String)
    enrollments = db.relationship('Enrollment', backref='course', cascade='all, delete-orphan')

class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    enrollment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    estudent_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    ecourse_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), nullable=False)

@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

@app.route('/student/create', methods=['GET', 'POST'])
def create_student():
    if request.method == 'POST':
        roll = request.form.get('roll')
        f_name = request.form.get('f_name')
        l_name = request.form.get('l_name')
        courses = request.form.getlist('courses')

        existing = Student.query.filter_by(roll_number=roll).first()
        if existing:
            return render_template('error.html', message="Student already exists. Please use different Roll Number!")

        new_student = Student(roll_number=roll, first_name=f_name, last_name=l_name)
        db.session.add(new_student)
        db.session.commit()

        for c_val in courses:
            course_id = int(c_val.replace('course_', ''))
            enrollment = Enrollment(estudent_id=new_student.student_id, ecourse_id=course_id)
            db.session.add(enrollment)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('create_student.html')

@app.route('/student/<int:student_id>')
def student_details(student_id):
    student = Student.query.get_or_404(student_id)
    enrollments = Enrollment.query.filter_by(estudent_id=student_id).all()
    courses = []
    for e in enrollments:
        course = Course.query.get(e.ecourse_id)
        if course:
            courses.append(course)
    return render_template('student_details.html', student=student, courses=courses)

@app.route('/student/<int:student_id>/update', methods=['GET', 'POST'])
def update_student(student_id):
    student = Student.query.get_or_404(student_id)
    if request.method == 'POST':
        student.first_name = request.form.get('f_name')
        student.last_name = request.form.get('l_name')
        
        Enrollment.query.filter_by(estudent_id=student_id).delete()
        courses = request.form.getlist('courses')
        for c_val in courses:
            course_id = int(c_val.replace('course_', ''))
            enrollment = Enrollment(estudent_id=student.student_id, ecourse_id=course_id)
            db.session.add(enrollment)
        db.session.commit()
        return redirect(url_for('index'))

    enrolled_course_ids = [e.ecourse_id for e in student.enrollments]
    return render_template('update_student.html', student=student, enrolled_course_ids=enrolled_course_ids)

@app.route('/student/<int:student_id>/delete')
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()

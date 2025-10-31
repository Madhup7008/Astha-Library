from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Student(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

class Book(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    copies = db.Column(db.Integer, nullable=False)

class Borrow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sid = db.Column(db.String(10), db.ForeignKey('student.id'), nullable=False)
    bid = db.Column(db.String(10), db.ForeignKey('book.id'), nullable=False)
    borrow_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date)
    fine = db.Column(db.Integer, default=0)

class Exam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sid = db.Column(db.String(10), db.ForeignKey('student.id'), nullable=False)
    exam = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Float, nullable=False)

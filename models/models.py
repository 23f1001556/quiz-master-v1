from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import controllers.config
import controllers.routes
from app import app

# Initializing the database
db = SQLAlchemy(app)

# Model for User
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    fullname = db.Column(db.String(80), nullable=False)
    qualification = db.Column(db.String(100))
    dob = db.Column(db.Date)
    isadmin = db.Column(db.Boolean, nullable=False, default=True)

class Subject(db.Model):
    __tablename__ = "subject"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    description = db.Column(db.String(100), nullable=False)
    chapters = db.relationship('Chapter', backref='subject', lazy=True)

class Chapter(db.Model):
    __tablename__ = "chapter"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    quizzes = db.relationship('Quiz', backref='chapter', lazy=True)
    questions = db.relationship('Question', backref='chapter', lazy=True)

class Quiz(db.Model):
    __tablename__ = "quiz"
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    date_of_quiz = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    time_duration = db.Column(db.String(5), nullable=False)  # hh:mm format
    remarks = db.Column(db.Text)
    questions = db.relationship('Question', backref='quiz', lazy=True)

class Question(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)  # Add this line
    question_statement = db.Column(db.Text, nullable=False)
    option_1 = db.Column(db.String(255), nullable=False)
    option_2 = db.Column(db.String(255), nullable=False)
    option_3 = db.Column(db.String(255), nullable=False)
    option_4 = db.Column(db.String(255), nullable=False)
    correct_option = db.Column(db.Integer, nullable=False)  # 1, 2, 3, or 4


class Scores(db.Model):
    __tablename__ = "scores"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    total_score = db.Column(db.Integer, nullable=False)

# Creating tables and adding default admin user
with app.app_context():
    db.create_all()

    # Create admin user if not exists
    existing_admin = User.query.filter_by(email='admin').first()
    if not existing_admin:
        admin = User(
            email='admin',
            password=generate_password_hash('admin'),
            fullname="Admin User",
            isadmin=True
        )
        db.session.add(admin)
        db.session.commit()

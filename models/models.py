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
    _password = db.Column("password", db.String(255), nullable=False)  # Store the hashed password here
    fullname = db.Column(db.String(80), nullable=False)
    qualification = db.Column(db.String(100))
    dob = db.Column(db.Date)
    isadmin = db.Column(db.Boolean, nullable=False, default=True)

    # Relationship with Scores
    scores = db.relationship('Scores', back_populates='user', cascade="all, delete-orphan")

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)  # Hash the password and store it in _password

    def check_password(self, password):
        return check_password_hash(self._password, password)  # Use _password for verification

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

    # Define the back_populates for the relationship
    user = db.relationship('User', back_populates='scores')


# Creating tables and adding default admin user
with app.app_context():
    db.create_all()

    # Create admin user if not exists
    existing_admin = User.query.filter_by(email='admin').first()
    if not existing_admin:
        hashed_password = generate_password_hash('admin')  # Hash the password before saving
        admin = User(
            email='admin',
            password=hashed_password,  # Save the hashed password
            fullname="Admin",
            isadmin=True
        )
        db.session.add(admin)
        db.session.commit()

from flask import Flask,render_template,redirect,request,url_for,flash,session
from app import app
from models.models import db,User,Subject,Chapter,Quiz,Question,Scores
from datetime import datetime
from functools import wraps
import os


def authcheck(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page')
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return wrapper


#login route and login post route
@app.route('/')
def login():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login_post():
    user_name = request.form.get('user_name')
    password = request.form.get('password')
    if user_name==' ' or password==' ':
        flash('username or password cannot be empty')
        return redirect(url_for('login'))
    user = User.query.filter_by(user_name=user_name).first()
    if not user:
        flash('User does not exist, please register')
        return redirect(url_for('login'))
    if not user.check_password(password):
        flash('Password is incorrect')
        return redirect(url_for('login'))
      # Both correct, successful login
    session['user_id']=user.id
    return redirect(url_for('home'))



#signup route and signup post route
@app.route('/signup')
def signup():
    return render_template ("signup.html")

@app.route('/signup', methods=['POST'])
def signup_post():
    user_name = request.form.get('user_name')
    password = request.form.get('password')
    email=request.form.get('email')
    if user_name == ' ' or password == ' 'or email=='':
        flash('Username or Password or Email cannot be empty')
        return redirect(url_for('register'))
    if User.query.filter_by(user_name=user_name).first():
        flash('User already exists')
        return redirect(url_for('login'))
    user=User(user_name=user_name,password=password,email=email)
    db.session.add(user)
    db.session.commit()
    flash('User registered successfully')
    return redirect(url_for('login'))

@app.route('/home')
@authcheck
def home():
    user=User.query.get(session['user_id'])
    if user.isadmin:
        return render_template("admin.html")
    else:
        return render_template('home.html')

@app.route('/admin')
@authcheck
def admin():
    user = User.query.get(session['user_id'])
    if not User.isadmin:
        flash('You are not authorized to view this page')
    return render_template("admin.html", User=user)

@app.route('/people')
@authcheck
def people():
    user = User.query.get(session['user_id'])
    if not user.isadmin:
        flash('You are not authorized to view this page')
    return render_template("people.html", User=user)


#navbar routes
@app.route('/signout')
def signout():
    session.pop('user_id',None)
    return redirect(url_for('login'))

@app.route('/profile')
@authcheck
def profile():
    user = User.query.get(session['user_id'])
    return render_template("profile.html", user=user)

@app.route('/profile',methods=['POST'])
@authcheck
def profile_post():
    user=User.query.get(session['user_id'])
    user_name=request.form.get('user_name')
    email=request.form.get('email')
    fullname=request.form.get('fullname')
    qualification=request.form.get('qualification')
    dob_str=request.form.get('dob')
    dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
    password=request.form.get('password')
    current_password=request.form.get('currentpassword')
    if not user.check_password(current_password):
        flash('current password is incorrect please try again!')
        return redirect(url_for('profile'))
    if User.query.filter_by(user_name=user_name).first() and user_name !=user.user_name:
         flash('Username already exists plaese choose another')
         return redirect(url_for('profile'))
    user.user_name=user_name
    user.email=email
    user.fullname=fullname
    user.qualification=qualification
    user.dob=dob
    user.password=password
    db.session.commit()
    flash('Profile updated successfully')
    return redirect(url_for('profile'))


#search mistake
@app.route('/search', methods=['GET'])
def search():
    # Ensure that the user is logged in and the session has a 'user_id'
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if no session
    
    # Get the current logged-in user
    current_user = User.query.get(session['user_id'])
    
    # Check if the logged-in user is an admin
    if current_user and current_user.isadmin:
        query = request.args.get('query')
        users = User.query.filter(User.user_name.ilike(f'%{query}%')).all()
        subjects = Subject.query.filter(Subject.name.ilike(f'%{query}%')).all()
        quizzes = Quiz.query.filter(Quiz.name.ilike(f'%{query}%')).all()
        
        # Return the results for admin users
        return render_template('search_results.html', users=users, query=query, user=current_user, subjects=subjects, quizzes=quizzes)
    
    # If the user is not an admin
    if current_user and not current_user.isadmin:
        query = request.args.get('query')
        subjects = Subject.query.filter(Subject.name.ilike(f'%{query}%')).all()
        quizzes = Quiz.query.filter(Quiz.name.ilike(f'%{query}%')).all()
        
        # Return the results for non-admin users (no users list)
        return render_template('search_results.html', query=query, user=current_user, subjects=subjects, quizzes=quizzes)
    
    # If somehow the user is not valid, return an error message (This shouldn't happen if session is properly set)
    return "User not found", 404
#search mistake ends
#admin dashboaard routes
@app.route('/subjects', methods=['GET', 'POST'])
def subjects():
    if request.method == 'POST':
        # Handle the form submission to add a new subject
        name = request.form.get('subject_name')
        
        # Check if the subject already exists
        existing_subject = Subject.query.filter_by(name=name).first()
        if existing_subject:
            flash('This subject already exists! Please try adding a different one.', 'error')
            return redirect(url_for('subjects'))  # Redirect back to the subjects page
        
        # If not, create a new subject and add it to the database
        new_subject = Subject(name=name)
        db.session.add(new_subject)
        db.session.commit()

        flash('Subject added successfully!', 'success')

    # Fetch all subjects after adding the new one (if any)
    subjects = Subject.query.all()

    # Render the template with the list of subjects
    return render_template('subjects.html', subjects=subjects)



# @app.route('/add_chapter', methods=['GET', 'POST'])
# def add_chapter():
#     if request.method == 'POST':
#         # Get data from the form
#         chapter_name = request.form.get('chapter_name')
#         description = request.form.get('description')
#         subject_id = request.form.get('subject_id')

#         # Create a new Chapter instance
#         new_chapter = Chapter(name=chapter_name, description=description, subject_id=subject_id)
        
#         # Add the new chapter to the session and commit to the database
#         db.session.add(new_chapter)
#         db.session.commit()

#         flash('Chapter added successfully!', 'success')
#         return redirect(url_for('subjects'))  # Redirect to the page showing all chapters (or anywhere else)

#     # If GET request, render the form to add a chapter
#     subjects = Subject.query.all()  # Get all subjects for the dropdown
#     return render_template('add_chapter.html', subjects=subjects)

# @app.route('/view_chapters')
# def view_chapters():
#     chapters = Chapter.query.all()  # Fetch all chapters
#     return render_template('view_chapters.html', chapters=chapters)


@app.route('/manage_users', methods=['GET'])
def manage_users_get():
    users = User.query.all()  # Get all users from the database
    return render_template('manage_users.html', users=users)  # Pass the users list to the template



@app.route('/report')
def report():
    return render_template('report.html')

@app.route('/quiz',methods=['POST'])
def quiz():
    return render_template('quiz.html')

@app.route('/quiz',methods=['POST'])
def quiz_post():

    return redirect(url_for('profile'))

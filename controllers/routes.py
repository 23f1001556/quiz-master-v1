from flask import Flask,render_template,redirect,request,url_for,flash,session
from app import app
from models.models import db,User,Subject,Chapter,Quiz,Question,Scores
from datetime import datetime
from functools import wraps
import os

#function to check loggin
def authcheck(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page')
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return wrapper
#function to check admin login
def admin_required(func):
    @wraps(func)
    def inner(*args,**kwargs):
        if 'user_id' not in session:
            flash('you need to login first')
            return redirect(url_for(login))
        user=User.query.get(session['user_id'])
        if not user.isadmin:
            flash ('You are not authorized to view this page')
            return redirect(url_for('home'))
        return func(*args,**kwargs)
    return inner 


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
#dashboard page for user and admin check role and redirect to user or admin
@app.route('/home')
@authcheck
def home():
    user=User.query.get(session['user_id'])
    if user.isadmin:
        return redirect(url_for('admin'))
    else:
        return redirect(url_for('people'))
#route for admin
@app.route('/admin')
@authcheck
def admin():
    user = User.query.get(session['user_id'])
    if not User.isadmin:
        flash('You are not authorized to view this page')
    return render_template("admin.html", User=user)
#route for user
@app.route('/people')
@authcheck
def people():
    user = User.query.get(session['user_id'])
    if user.isadmin:
        flash("Not authorized to vie this page")
        return redirect(url_for('home'))
    return render_template("home.html", User=user)

#navbar routes singout
@app.route('/signout')
def signout():
    session.pop('user_id',None)
    return redirect(url_for('login'))

#edit profile route
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
    return render_template('search_results.html')
#search mistake ends

#report route 
@app.route('/report',methods=['GET'])
@authcheck
@admin_required
def report():
    return render_template('report.html')

#admin dashboaard routes-subjects
@app.route('/admin_subjects', methods=['GET', 'POST'])
@authcheck
@admin_required
def admin_subjects():
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
    return render_template('admin_subjects.html', subjects=subjects)


@app.route('/admin_subjects/<int:id>/edit')
@authcheck
@admin_required
def edit_subject(id):
    return render_template('subject/edit.html')
@app.route('/admin_subjects/<int:id>/delete')
@authcheck
@admin_required
def delete_subject(id):
    return render_template('subject/delete.html')

# @app.route('/admin_subjects/<int:id>/delete',methods=['POST'])
# @authcheck
# @admin_required
# def delete_subject(id):
#     subject=Subject.query.get(id)
#     if not subject:
#         flash('subject doesnot exists')
#         return redirect(url_for(admin_subjects))
#     db.session.delete(subject)
#     db.session.commit()
#     flash("subject deleted successfully")
#     return redirect(url_for(admin))

#admin dashboaard routes-chapters
@app.route('/chapter',methods=['GET','POST'])
@authcheck
@admin_required
def admin_chapters():

    return render_template('admin_chapters.html')

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


# @app.route('/admin_chapters/<int:id>/edit')
# @authcheck
# @admin_required
# def edit_subject(id):
#     return render_template('chapter/delete.html')

# @app.route('/admin_chapters/<int:id>/delete')
# @authcheck
# @admin_required
# def delete_subject(id):
#     return render_template('chapter/delete.html')

#admin dashboaard routes-quiz
@app.route('/quiz',methods=['GET','POST'])
@authcheck
@admin_required
def admin_quiz():
    return render_template('admin_quiz.html')

#admin dashboaard routes-manage_users
@app.route('/manage_users', methods=['GET'])
@authcheck
@admin_required
def manage_users_get():
    users = User.query.all()  # Get all users from the database
    return render_template('manage_users.html', users=users)  # Pass the users list to the template


#user subejct routes
@app.route('/user_subjects', methods=['GET'])
@authcheck
def subjects():
    subjects = Subject.query.all()  # Fetch all subjects from the database
    return render_template('subjects.html', subjects=subjects)

#user quiz routes
@app.route('/quiz',methods=['POST'])
@authcheck
def quiz():
    return render_template('quiz.html')
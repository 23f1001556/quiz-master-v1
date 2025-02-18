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
        return redirect(url_for('signup'))
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
    return render_template("home.html", user=user)

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
    query = request.args.get('search-query', '')  # Ensure it's a string
    users = []
    subjects = []
    chapters = []
    quiz = []

    if query:
        # Search users
        users = User.query.filter(
            (User.user_name.ilike(f'%{query}%')) | 
            (User.fullname.ilike(f'%{query}%'))
        ).all()

        # Search subjects
        subjects = Subject.query.filter(
            (Subject.name.ilike(f'%{query}%'))
        ).all()

        # Search chapters
        chapters = Chapter.query.filter(
            (Chapter.name.ilike(f'%{query}%'))  # Assuming 'name' is the field you're searching on
        ).all()

        # Search quiz
        quiz = Quiz.query.filter(
            (Quiz.name.ilike(f'%{query}%'))
        ).all()

    return render_template('search_results.html', query=query, users=users, subjects=subjects, chapters=chapters, quiz=quiz)




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

#edit subjects 
@app.route('/admin_subjects/<int:id>/edit', methods=['GET', 'POST'])
@authcheck
@admin_required
def edit_subject(id):
    subject = Subject.query.get(id)  # Use id to get the subject
    if not subject:
        flash('Subject does not exist.')
        return redirect(url_for('admin_subjects'))

    # Handle POST request to update subject
    if request.method == 'POST':
        new_name = request.form['subject_name']  # Get the new name from the form
        if new_name:
            subject.name = new_name  # Update the subject's name
            db.session.commit()
            flash('Subject updated successfully.')
            return redirect(url_for('admin_subjects'))  # Redirect after update

    return render_template('subject/edit.html', subject=subject)

#deleting subjects 
@app.route('/admin_subjects/<int:id>/delete')
@authcheck
@admin_required
def delete_subject(id):
    subject=Subject.query.get(id)
    if not subject:
        flash ("subject doesnot exists")
        return redirect(url_for('admin_subjects'))
    if subject:
        db.session.delete(subject)
        db.session.commit()
        flash(" subject deleted successfully")
        return redirect(url_for('admin_subjects'))
    return render_template('subject/delete.html')






#admin dashboaard routes-chapters
@app.route('/chapter', methods=['GET', 'POST'])
@authcheck
@admin_required
def admin_chapters():
    if request.method == 'GET':
        subjects = Subject.query.all()  # Get all subjects
        chapters = Chapter.query.all()  # Get all chapters
        return render_template('admin_chapters.html', subjects=subjects, chapters=chapters)

    if request.method == 'POST':
        subject_id = request.form.get('subject')
        chapter_name = request.form.get('chapter_name')

        # Validate and add new chapter
        if subject_id and chapter_name:
            new_chapter = Chapter(name=chapter_name, subject_id=subject_id)
            db.session.add(new_chapter)
            db.session.commit()
            flash('Chapter added successfully!')
        
        return redirect(url_for('admin_chapters'))




#edit chapter


#edit quiz



#admin dashboaard routes-quiz


@app.route('/quiz', methods=['GET', 'POST'])
@authcheck
@admin_required
def admin_quiz():
    if request.method == 'POST':
        # Capture form data
        subject_id = request.form.get('subject')
        chapter_id = request.form.get('chapter')
        quiz_name = request.form.get('quiz_name')

        # Create a new quiz object
        new_quiz = Quiz(name=quiz_name, chapter_id=chapter_id)

        # Add the quiz to the session and commit to the database
        db.session.add(new_quiz)
        db.session.commit()

        # Flash success message
        flash('Quiz added successfully!', 'success')

        # Redirect to the quiz management page (to avoid form resubmission)
        return redirect(url_for('admin_quiz'))

    # GET request: Retrieve subjects and chapters to display in the form
    subjects = Subject.query.all()
    return render_template('admin_quiz.html', subjects=subjects)



@app.route('/quiz_form')
def quiz_form():
    return render_template('quiz_form.html')



#admin dashboaard routes-manage_users
@app.route('/manage_users', methods=['GET'])
@authcheck
@admin_required
def manage_users():
    users = User.query.all()  # Get all users from the database
    return render_template('manage_users.html', users=users)  # Pass the users list to the template

#deleting users

@app.route('/manage_users_delete/<int:id>', methods=['POST'])
def manage_users_delete(id):
    user = User.query.get(id)  # Fetch the user from the database
    if not user:
        flash('User not found.')
        return redirect(url_for('manage_users'))

    # Check if the user is an admin
    if user.user_name == "admin":  # Assuming "admin" is a user_name identifier
        flash('Master user cannot be deleted.')
        return redirect(url_for('manage_users'))
    
    # Delete the user
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully.')

    # Redirect to the user management page
    return redirect(url_for('manage_users'))



#admin manage_score ->score button

@app.route('/check_score')
def check_score():
    # Fetch the user score details based on the user_id from the session or query string
    user_id = request.args.get('user_id')  # Assuming user_id is passed as a query parameter
    if user_id:
        scores = Scores.query.filter_by(user_id=user_id).all()
    else:
        scores = None
    
    return render_template('manage_users/score.html', scores=scores)


@app.route('/dashboard')
@authcheck
@admin_required
def dashboard():
    return render_template('dashboard.html')

#user subejct routes
@app.route('/user_subjects', methods=['GET'])
@authcheck
def subjects():
    subjects = Subject.query.all()  # Fetch all subjects from the database
    return render_template('subjects.html', subjects=subjects)

#user quiz routes
@app.route('/quiz/<int:quiz_id>/add_question', methods=['GET', 'POST'])

def add_question(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return "Quiz not found", 404

    if request.method == 'POST':
        question_statement = request.form.get('question_statement')
        option_1 = request.form.get('option_1')
        option_2 = request.form.get('option_2')
        option_3 = request.form.get('option_3')
        option_4 = request.form.get('option_4')
        correct_option = request.form.get('correct_option')

        # Create new Question object
        new_question = Question(
            quiz_id=quiz.id,
            chapter_id=quiz.chapter_id,
            question_statement=question_statement,
            option_1=option_1,
            option_2=option_2,
            option_3=option_3,
            option_4=option_4,
            correct_option=int(correct_option)  # Ensure correct_option is an integer (1-4)
        )

        # Add the question to the database
        db.session.add(new_question)
        db.session.commit()

        # Redirect to the quiz page after adding the question
        return redirect(url_for('admin_quiz', quiz_id=quiz.id))

    return render_template('quiz_form.html', quiz=quiz)


#user report route
@app.route('/user_report')
@authcheck
def user_report():
    return render_template('user_report.html')



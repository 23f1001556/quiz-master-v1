from flask import Flask,render_template,redirect,request,url_for,flash,session
from app import app
from models.models import db,User,Subject,Chapter,Quiz,Question,Scores
from functools import wraps
import os



#login route and login post route
@app.route('/')
def login():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('username')
    password = request.form.get('password')
    if email==' ' or password==' ':
        flash('username or password cannot be empty')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=email).first()
    if not user:
        flash('User does not exist, please register')
        return redirect(url_for('login'))
    if not user.check_password(password):
        flash('Password is incorrect')
        return redirect(url_for('login'))
      # Both correct, successful login
    session['user_id']=user.id
    return render_template('home.html')



#signup route and signup post route
@app.route('/signup')
def signup():
    return render_template ("signup.html")

@app.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('username')
    password = request.form.get('password')
    name=request.form.get('fullname')
    if email == ' ' or password == ' ' or name==' ':
        flash('username or password or name cannot be empty')
        return redirect(url_for('register'))
    if User.query.filter_by(email=email).first():
        flash('User already exists')
        return redirect(url_for('login'))
    user=User(email=email,password=password,fullname=name)
    db.session.add(user)
    db.session.commit()
    flash('User registered successfully')
    return redirect(url_for('login'))

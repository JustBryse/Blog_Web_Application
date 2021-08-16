from flask import Blueprint, render_template, redirect, url_for, request
from flask import *
from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint("auth",__name__)

@auth.route("/",methods=["GET","POST"])
@auth.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # look for email that matches the login form email
        user = User.query.filter_by(email=email).first()
        # if the user exists, check the passwords, but hash the login form password first.
        # the hashed password in the User Model table hast to be compared with the hash of the login form password
        if user:
            is_verified = check_password_hash(user.password,password)
            print(generate_password_hash(password,method="sha256"))
            print(user.password)
            print(is_verified)
            if is_verified:
                login_user(user,remember=True)
                flash("Logged in.",category="success")
                return redirect(url_for("views.home"))
            else:
                flash("Password is incorrect.",category="error")
        else:
            flash("Email does not exist.",category="error")

    return render_template("login.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route("/signup",methods=["GET","POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        # look in user model (table) to find the first instance in the email and username column that matches the data from the signup form
        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        # the signup data must conform too these conditions
        if email_exists:
            flash("This email already exists.",category="error")
        elif len(email) < 10:
            flash("This email is invalid",category="error")
        elif username_exists:
            flash("This username already exists.",category="error")
        elif len(username) < 2:
            flash("Username is too short.",category="error")
        elif password1 != password2:
            flash("Passwords do not match.",category="error")
        elif len(password1) < 6:
            flash("Password is too short.",category="error")
        else:
            # hash the password
            new_user = User(email=email,username=username,password=generate_password_hash(password1,method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            #login_user(new_user,remember=True)
            flash("User created.")
            return redirect(url_for("auth.login")) # change the url to localhost:port/home

    return render_template("signup.html")

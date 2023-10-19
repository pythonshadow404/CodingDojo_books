from flask_app import app
from flask_app.models.user_model import User
from flask import Flask, render_template, redirect, request, session , flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/register', methods = ["POST"])
def register():
    if not User.validate_user(request.form):
        return redirect("/")
    #hash your password before going to the dashboard
    pw_hash = bcrypt.generate_password_hash(request.form["password"])
    #format all of our data from our form 
    data = {
        "username": request.form["username"],
        "email": request.form["email"],
        "password":pw_hash
    }
    #check to see if our email already exists in our database
    if User.get_by_email(data):
        flash("Email already in use!")
        return redirect("/")
    else:
        user_id = User.save(data)
        session["user_id"] = user_id
        return redirect("/dashboard")

@app.route("/login", methods = ["POST"])
def login():
    data = {
        "email":request.form["email"]
    }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        flash("Invalid Email/Password")
        return redirect("/")
    # if user is already in the db and p/w matches
    session["user_id"] = user_in_db.id
    return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
    # Make sure user is logged in in order for them to be in the dashboard.
    if not session.get("user_id"): #if nobody is logged-in redirect by to the index
        return redirect("/")
    #If someone is logged in, let's get that user data
    # anytime we query the db we to to store things in data
    data = {
        "id":session["user_id"]
    }
    user = User.get_by_id(data)
    return render_template("dashboard.html", user = user)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


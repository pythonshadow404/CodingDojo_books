from flask_app import app
from flask import render_template, redirect, session

@app.route("/")
def home():
    # If we are already logged in, we will /forward-slash route to our home page (our dashboard)
    if session.get("user_id"):
        return redirect("/dashboard")
    return render_template("index.html")

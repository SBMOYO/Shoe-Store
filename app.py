import sqlite3
import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps


app = Flask(__name__)

app.secret_key = 'my_secret_key'
app.config['SESSION_COOKIE_NAME'] = 'online_shoe_store'

#db = sqlite3.connect("main.db")

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///main.db")

def login_required(f):
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/logIn", methods = ["GET", "POST"])
def log_in():

    error = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE email = ?;", username)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], password):
            error = "Invalid email or password"
        else:
            # Redirect user to home page
            return redirect("/")
    
    return render_template("logIn.html", error=error)


@app.route("/register", methods = ["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # Create a table
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
            )
        """)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?;", username)

         # Ensure the username name does not already exist
        if len(rows) != 0:
            return redirect("logIn.html")

        # Insert username into database
        id = db.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?);",
                        username, email, generate_password_hash(password))
        
        return redirect("/")
        
    else:
        return render_template("register.html")



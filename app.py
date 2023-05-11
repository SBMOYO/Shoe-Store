import sqlite3
import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from flask import jsonify


app = Flask(__name__)

app.secret_key = 'my_secret_key'
app.config['SESSION_COOKIE_NAME'] = 'online_shoe_store'
app.config['IMAGE_UPLOADS'] = 'static/assets/uploads'

#db = sqlite3.connect("main.db")

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///main.db")

def login_required(f):
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("id") is None:
            return redirect("/logIn")
        return f(*args, **kwargs)
    return decorated_function


def admin_login_required(f):
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("admin_id") is None:
            return redirect("/admin")
        return f(*args, **kwargs)
    return decorated_function


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():


    # Query database for shoes
    rows = db.execute("SELECT * FROM shoe_stock;")

    return render_template("index.html", rows=rows)


@app.route("/logIn", methods = ["GET", "POST"])
def logIn():

    # forget previous user
    session.clear()

    error = None

    if request.method == "POST":

        if not request.form.get("username"):
            error = "Invalid username"

        if not request.form.get("password"):
            error = "Invalid password"

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?;", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            error = "Invalid username or password"

        else:

            # assign id to session
            session['id'] = rows[0]['id']

             # Redirect user to home page
            return redirect("/")
    
    return render_template("logIn.html", error=error)


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/logIn")


@app.route("/admin", methods = ["GET", "POST"])
def admin():

    # forget previous user
    session.clear()

    error = None

    if request.method == "POST":

        if not request.form.get("username"):
            error = "Invalid username"

        if not request.form.get("password"):
            error = "Invalid password"

        # Query database for username
        rows = db.execute("SELECT * FROM admin_users WHERE username = ? and password = ?;", request.form.get("username"), request.form.get("password"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not request.form.get("password"):
            error = "Invalid username or password"

        else:

            # assign id to session
            session['admin_id'] = rows[0]['admin_id']

            
             # Redirect user to home page
            return redirect("/upload")
    
    return render_template("admin.html", error=error)


@app.route("/register", methods = ["GET", "POST"])
def register():

    error = None

    # forget previous user
    session.clear()

    if request.method == "POST":

        if not request.form.get("username"):
            error = "Please provide username"

        if not request.form.get("email"):
            error = "Please provide email address"

        if not request.form.get("password"):
            error = "Please provide password"

        if not request.form.get("confirm_password"):
            error = "Please confirm password"

        if request.form.get('password') != request.form.get('confirm_password'):
            error = "password not matching"

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
        rows = db.execute("SELECT * FROM users WHERE username = ?;", request.form.get('username'))

         # Ensure the username name does not already exist
        if len(rows) != 0:
            error = "Username already taken"

        # Insert username into database
        id = db.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?);",
                        request.form.get('username'), request.form.get('email'), generate_password_hash(request.form.get('password')))
        
        session['id'] = rows[0]['id']
        
        return redirect("/")
        
    else:
        return render_template("register.html", error=error)


@app.route("/upload", methods=["GET", "POST"])
@admin_login_required
def upload():

    error = None    

    if request.method == "POST":

        if not request.form.get("shoe_name"):
            error = "Please provide shoe name"

        if not request.form.get("price"):
            error = "Please provide the price"

        if not request.form.get("shoe_colour"):
            error = "What colour is the shoe"

        if request.files:
            image = request.files.get("image")

            if not image:
                error = "Please provide image file"
            
            image.save(os.path.join(app.config['IMAGE_UPLOADS'], image.filename))
  
        # Create a table
        db.execute("""
            CREATE TABLE IF NOT EXISTS shoe_stock (
            shoe_id INTEGER AUTO_INCREMENT PRIMARY KEY,
            shoe_name TEXT NOT NULL,
            price INTEGER NOT NULL,
            shoe_colour INTEGER NOT NULL,
            shoe_image TEXT NOT NULL
            )
        """)

          # Query database for username
        rows = db.execute("SELECT * FROM shoe_stock WHERE shoe_name = ?;", request.form.get("shoe_name"))

         # Ensure the username name does not already exist
        if len(rows) != 0:

            # Insert shoe details into database
            id = db.execute("UPDATE shoe_stock SET price = ?, shoe_colour = ? WHERE shoe_name = ?;",
                            request.form.get("price"), request.form.get("shoe_colour"), request.form.get('shoe_name'))
        # Insert shoe details into database
        id = db.execute("INSERT INTO shoe_stock (shoe_name, price, shoe_colour, shoe_image) VALUES (?,  ?, ?, ?);",
                        request.form.get("shoe_name"), request.form.get("price"), request.form.get("shoe_colour"), image.filename)
        
        return redirect("/")
        

    return render_template("upload.html", error=error)


@app.route("/cart", methods=["GET", "POST"])
@login_required
def cart():

    if request.method == "POST":

        shoe_id = request.form.get("shoe_id")

        new = db.execute("INSERT INTO kart (userId, shoeId) VALUES (?, ?);", session.get('id'), shoe_id)

        return redirect("/")
            
            
       

    rows = db.execute("SELECT * FROM shoe_stock WHERE shoe_id IN (SELECT shoeId FROM kart WHERE userId = ?);", session.get('id'))
    print(rows)
    return render_template("cart.html", rows=rows)


@app.route("/remove_from_cart", methods=["POST"])
@login_required
def remove_from_cart():

    shoe_id = request.form.get('shoe_id')

    row = db.execute("DELETE FROM kart WHERE userId = ? AND shoeId = ?;", session.get('id'), shoe_id)

    return redirect("/cart")


@app.route("/delete_account", methods=["POST"])
@login_required
def delete_account():
    try:
        db.execute("DELETE FROM users WHERE id = ?;", session.get('id'))
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
from flask import Flask 
from flask import render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/logIn")
def log_in():
    return render_template("logIn.html")


@app.route("/register")
def register():
    return render_template("register.html")



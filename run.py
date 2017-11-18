import os
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/', methods=["GET", "POST"])
def homepage():  
	return render_template('homepage.html')

@views.route('/register', methods=["GET", "POST"])
def register():
	if request.method == "POST":
		return redirect("/")
	else:
		return render_template('register.html')

@views.route('/login', methods=["GET", "POST"])
def login():
	if request.method == "POST":
		return redirect("/")
	else:
		return render_template('login.html')
	
@views.route('/create', methods=["GET", "POST"])
def create():
	if request.method == "POST":
		return redirect("/")
	else:
		return render_template('create.html')

# go to localhost:8000 to view
if 'DEBUG' in os.environ:
    app.run(host = '0.0.0.0', port = 8000)

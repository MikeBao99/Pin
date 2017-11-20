import os
from helpers import *
from sqlalchemy import create_engine
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

# Configure PostgreSQL database using SQLAlchemy
db = create_engine('postgres://lgexotyvoyetfh:0c61846252d51c314b5f925d9729ad5bc818ca97deb54cc9592759bfe4e2e2ab@ec2-107-20-214-99.compute-1.amazonaws.com:5432/d223jo1u4l3s6f')

@app.route('/', methods=["GET", "POST"])
def homepage():  
	return render_template('homepage.html')

@app.route('/register', methods=["GET", "POST"])
def register():
	if request.method == "POST":
		# Ensure username was submitted
		if not request.form.get("username"):
			return render_template("error.html")
		# Ensure password was submitted
		if not request.form.get("password"):
			return render_template("error.html")
		if not request.form.get("confirmation"):
			return render_template("error.html")

		if request.form.get("password") != request.form.get("confirmation"):
			return render_template("error.html")
		password_hash = generate_password_hash(request.form.get("password"))
		result = db.execute("INSERT INTO users (username, hash) VALUES('%s', '%s')" % (request.form.get("username"), password_hash))
		if not result:
			# check if username is valid
			return render_template("error.html")
		row = db.execute("SELECT * FROM users WHERE username = '%s'" % (request.form.get("username")))
		session["user_id"] = row.fetchone()["id"]
		return redirect("/")
	else:
		return render_template("register.html")

@app.route('/login', methods=["GET", "POST"])
def login():
	# Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("error.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("error.html")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = '%s'" % (request.form.get("username")))
	first = rows.fetchone()
        # Ensure username exists and password is correct
        if not first or not check_password_hash(first["hash"], request.form.get("password")):
            return render_template("error.html")

        # Remember which user has logged in
        session["user_id"] = 1

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route('/create', methods=["GET", "POST"])
@login_required	
def create():
	if request.method == "POST":
		return redirect("/")
	else:
		return render_template('create.html')

@app.route('/manage', methods=["GET", "POST"])
def manage():
	if request.method == "POST":
		return redirect("/")
	else:
		return render_template('manage.html')


# go to localhost:8000 to view
if 'DEBUG' in os.environ:
	app.run(host = '0.0.0.0', port = 8000)

import os
import sys
from helpers import *
from sqlalchemy import create_engine
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# Set up Flask Session
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)




# Configure PostgreSQL database using SQLAlchemy
db = create_engine('postgres://lgexotyvoyetfh:0c61846252d51c314b5f925d9729ad5bc818ca97deb54cc9592759bfe4e2e2ab@ec2-107-20-214-99.compute-1.amazonaws.com:5432/d223jo1u4l3s6f')

# Renders Homepage
@app.route('/', methods=["GET", "POST"])
def homepage():  
    return render_template('homepage.html')

# Renders and handles submission of Register page
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("error.html", error = "Please provide username!")
        # Ensure password was submitted
        if not request.form.get("password"):
            return render_template("error.html", error = "Please provide password!")
        if not request.form.get("confirmation"):
            return render_template("error.html", error = "Please provide password confirmation!")
        # Ensure that passwords match
        if request.form.get("password") != request.form.get("confirmation"):
            return render_template("error.html", error = "Passwords do not match!")
        password_hash = generate_password_hash(request.form.get("password"))
        try:
            db.execute("INSERT INTO users (username, hash) VALUES('%s', '%s')" % (request.form.get("username"), password_hash))
        except:
            # check if username is valid
            return render_template("error.html", error="Username already exists!")
        row = db.execute("SELECT * FROM users WHERE username = '%s'" % (request.form.get("username")))
        session["user_id"] = row.fetchone()["username"]
        return redirect("/")
    else:
        return render_template("register.html")

# Logs users in, renders login.html and handles form submission
@app.route('/login', methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get('username')
        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("error.html", error = "Please provide username!")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("error.html", error = "Please provide password!")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = '%s'" % (request.form.get("username")))
        first = rows.fetchone()
        # Ensure username exists and password is correct
        if not first or not check_password_hash(first["hash"], request.form.get("password")):
            return render_template("error.html", error="Incorrect username and password!")

        # Remember which user has logged in
        session["user_id"] = username
        flash("You have been logged in!")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

# Renders an error page
@app.route('/error', methods=["GET"])
def error():
       return render_template("error.html")

# Renders the Create Event page and handles form submission
@app.route('/create', methods=["GET", "POST"])
@login_required 
def create():
    if request.method == "POST":

        if not request.form.get("class"):
            return render_template("error.html", error = "Please provide class!")
        if not request.form.get("location"):
            return render_template("error.html", error = "Please provide location!")
        if not request.form.get("startDatetime"):
            return render_template("error.html", error = "Please provide start time!")
        if not request.form.get("endDatetime"):
            return render_template("error.html", error = "Please provide end time!")

        if request.form.get("startDatetime") < datetime.now().strftime('%Y-%m-%d %H:%M:%S'):
            return render_template("error.html", error = "Selected start time has already passed!")

        if request.form.get("endDatetime") < datetime.now().strftime('%Y-%m-%d %H:%M:%S'):
            return render_template("error.html", error = "Selected end time has already passed!")

        if request.form.get("startDatetime") > request.form.get("endDatetime"):
            return render_template("error.html", error = "End time must come after start time!")

        #row = db.execute("SELECT * FROM users WHERE session["user_id"] = '%s'" % (request.form.get("username")))
        name = session["user_id"]

        db.execute("INSERT INTO events (name, class, starttime, endtime, location) VALUES('%s', '%s', '%s', '%s', '%s')" % 
            (name, request.form.get("class"),  request.form.get("startDatetime"), 
                request.form.get("endDatetime"), request.form.get("location")))
        print "\n\n\n"
        print request.form.get("startDatetime")
        print "\n\n\n"
        sys.stdout.flush()
        return redirect("/")
    else:
        return render_template('create.html')
    
# Handles the search function, searches through the SQL database with several conditions
@app.route('/search', methods=["GET", "POST"])
def search():
    if request.method == "POST":
        # Store user search request
        q = "%%" + request.form.get("search") + "%%"
        # Query Database
        eventsrow = db.execute("SELECT * FROM events WHERE LOWER(class) LIKE LOWER('%s') ORDER BY starttime ASC" % (q))
        events = []
        row = eventsrow.fetchone()
        while row:
            events.append(row)
            row = eventsrow.fetchone()
        return render_template('search.html', events = events)
    else:
        # Prints out all events in a table, Query database
        eventsrow = db.execute("SELECT * FROM events ORDER BY starttime ASC")
        events = []
        row = eventsrow.fetchone()
        while row:
            events.append(row)
            row = eventsrow.fetchone()
        return render_template('search.html', events = events)

# Handles the manage 
@app.route('/manage', methods=["GET", "POST"])
def manage():
    eventsrow = db.execute("SELECT * FROM events WHERE name = '%s'" % (session["user_id"]))
    events = []
    row = eventsrow.fetchone()
    while row:
        events.append(row)
        row = eventsrow.fetchone()
    return render_template('manage.html', events = events, name = session["user_id"])

# Handles Edit if a user chooses to edit a page from the Manage Events page
@app.route('/edit', methods=["GET", "POST"])
def edit():
    if request.form.get("type") == "post":
        print request.form.get("startDatetime") + "\n\n"
        sys.stdout.flush()
        # Update the database
        db.execute("UPDATE events SET class = '%s', location = '%s', starttime = '%s', endtime = '%s' WHERE id = '%s'" % (request.form.get('class'), request.form.get('location'), request.form.get('startDatetime'), request.form.get('endDatetime'), request.form.get('id')))
        return redirect("/manage")
    else:
        # Render the form for editing
        val = request.form.get("edit")
        eventsrow = db.execute("SELECT * FROM events WHERE id = '%s'" % (val))
        events= eventsrow.fetchone()
        return render_template('edit.html', events = events, starttime = replace_spaces(str(events["starttime"])), endtime = replace_spaces(str(events["endtime"])))

# Handles deletion of an event    
@app.route('/delete', methods=["GET", "POST"])
def delete():
    val = request.form.get('delete')
    # Delete event from database
    db.execute("DELETE FROM events WHERE id = '%s'" % (val))
    return redirect('/manage')


# go to localhost:8000 to view
if 'DEBUG' in os.environ:
    app.run(host = '0.0.0.0', port = 8000)

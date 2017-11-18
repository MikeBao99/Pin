from flask import * #TODO: actually look at imports
import requests
import json
import urllib
from werkzeug import * #TODO: actually look at imports

views = Blueprint('views', __name__)
views.config["SESSION_FILE_DIR"] = mkdtemp()
views.config["SESSION_PERMANENT"] = False
views.config["SESSION_TYPE"] = "filesystem"
Session(views)


extensions = set(['jpg'])

@views.route('/', methods=["GET", "POST"])
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
	
@views.route('/about')
def about():
	return render_template('about.html')


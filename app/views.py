from flask import * #TODO: actually look at imports
import requests
import json
from tempfile import mkdtemp
import urllib
from werkzeug import * #TODO: actually look at imports

views = Blueprint('views', __name__)


extensions = set(['jpg'])

@app.route('/', methods=["GET", "POST"])
def homepage():
	return render_template('homepage.html')

@app.route('/register', methods=["GET", "POST"])
def register():
	if request.method == "POST":
		return redirect("/")
	else:
		return render_template('register.html')

@app.route('/login', methods=["GET", "POST"])
def login():
	if request.method == "POST":
		return redirect("/")
	else:
		return render_template('login.html')
	
@app.route('/create', methods=["GET", "POST"])
def create():
	if request.method == "POST":
		return redirect("/")
	else:
		return render_template('create.html')
	
@app.route('/about')
def about():
	return render_template('about.html')


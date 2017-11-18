from flask import * #TODO: actually look at imports
import boto3
import requests
import json
import urllib
from werkzeug import * #TODO: actually look at imports
import classify as watson

views = Blueprint('views', __name__)

extensions = set(['jpg'])

@views.route('/', methods=["GET", "POST"])
def homepage():
	return render_template('homepage.html')
  
@views.route('/about')
def about():
	return render_template('about.html')


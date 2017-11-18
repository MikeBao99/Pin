import os
from flask import *

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def homepage():  
	return render_template('homepage.html')

# go to localhost:8000 to view
if 'DEBUG' in os.environ:
    app.run(host = '0.0.0.0', port = 8000)

from app import app
import os
from Flask import *

app = Flask(__name__)

# go to localhost:8000 to view
if 'DEBUG' in os.environ:
    app.run(host = '0.0.0.0', port = 8000)

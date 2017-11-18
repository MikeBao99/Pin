from app import app
from app.views import views

import os

app.register_blueprint(views)

# go to localhost:8000 to view
if 'DEBUG' in os.environ:
    app.run(host = '0.0.0.0', port = 8000)

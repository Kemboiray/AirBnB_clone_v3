#!/usr/bin/python3
"""Creating a web application and
   impressing blueprints on it"""

import os
from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def session_teardown(exc):
    """Closing the current session"""
    storage.close()


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST')
    port = os.getenv('HBNB_API_PORT')
    app.run(host=host, port=port,
            debug=False, threaded=True)

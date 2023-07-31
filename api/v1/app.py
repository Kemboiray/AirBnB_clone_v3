#!/usr/bin/python3
"""Creating a web application and
   impressing blueprints on it"""

from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def session_teardown():
    """Closing the current session"""
    storage.close()


if __name__ == "__main__":
    app.run(host='HBNB_API_HOST', port='HBNB_API_PORT',
            debug=False, threaded=True)

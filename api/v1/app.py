#!/usr/bin/python3
"""Creating a web application and
   impressing blueprints on it"""

import os
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def session_teardown(exc):
    """Closing the current session"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handling not found error"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST')
    port = os.getenv('HBNB_API_PORT')
    app.run(host=host, port=port,
            debug=False, threaded=True)

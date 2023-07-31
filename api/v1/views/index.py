#!/usr/bin/python3
"""Checking the response status code"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False, methods=['GET'])
def response_status():
    """Returning the status of the response"""
    return jsonify({"status": "OK"})

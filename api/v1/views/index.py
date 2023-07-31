#!/usr/bin/python3
"""Checking the response status code"""

from app_views import api.v1.views
from flask import jsonify


@app_views.route('/status')
def response_status():
    """Returning the status of the response"""
    return jsonify(({"status": "OK"}), 200)

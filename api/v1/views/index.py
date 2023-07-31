#!/usr/bin/python3
"""Checking the response status code"""

from api.v1.views import app_views
from models import storage
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', strict_slashes=False, methods=['GET'])
def response_status():
    """Returning the status of the response"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False, methods=['GET'])
def object_count():
    """Retrieve object count"""
    classes = {"amenities": Amenity, "cities": City, "places": Place,
               "reviews": Review, "states": State, "users": User}
#   obj_count = {}
#   for k, v in classes.items():
#       count = storage.count(v)
#       obj_count[k] = count
    return jsonify({k, storage.count(v) for k, v in classes.items()})

#!/usr/bin/python3
"""Defines a view for `City` objects"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models.city import City
from models import storage


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['GET'])
def get_cities(state_id):
    """Retrieve the list of `City` objects subclassing a `State` object"""
    state = [s for s in storage.all(State).values() if s.id == state_id]
    if not state:
        abort(404)
    city_list = [c.to_dict() for c in storage.all(City).values()
                 if c.state_id == state_id]
    return jsonify(city_list)


@app_views.route('/cities/<city_id>',
                 strict_slashes=False, methods=['GET'])
def get_city(city_id):
    """Retrieve a `City` object"""
    city = [c for c in storage.all(City).values() if c.id == city_id]
    if not city:
        abort(404)
    return jsonify(city[0].to_dict())


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_city(city_id):
    """Delete a `City` object, given its `id`"""
    city = [c for c in storage.all(City).values() if c.id == city_id]
    if city:
        storage.delete(city[0])
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['POST'])
def create_city(state_id):
    """Create a `City` object"""
    state = [s for s in storage.all(State).values() if s.id == state_id]
    if not state:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if "name" not in data:
        abort(400, description="Missing name")
    city_obj = City(**data)
    city_obj.save()
    return jsonify(city_obj.to_dict()), 201


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['PUT'])
def update_city(city_id):
    """Update a `City` object, given its `id`"""
    city = [c for c in storage.all(City).values() if c.id == city_id]
    if city:
        data = request.get_json()
        if not data:
            abort(400, description="Not a JSON")
        for key, value in data.items():
            if key not in ("id", "state_id", "created_at", "uppdated_at"):
                setattr(city[0], key, value)
        city[0].save()
        return jsonify(city[0].to_dict()), 200
    abort(404)


@app_views.errorhandler(404)
def not_found(error):
    """Handling not found error"""
    return jsonify({"error": "Not found"}), 404

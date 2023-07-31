#!/usr/bin/python3
"""Defines a view for `Place` objects"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User
from models.city import City
from models.place import Place
from models import storage


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['GET'])
def get_places(city_id):
    """Retrieve the list of `Place` objects"""
    city = [c for c in storage.all(City).values() if c.id == city_id]
    if city:
        place = []
        for p in storage.all(Place).values():
            if p.city_id == city_id:
                place.append(p.to_dict())
        return jsonify(place)
    abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['GET'])
def get_place(place_id):
    """Retrieve a `Place` object, given its `id`"""
    place = [p for p in storage.all(Place).values() if p.id == place_id]
    if place:
        place_dict = place[0].to_dict()
        return jsonify(place_dict)
    abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_place(place_id):
    """Delete a `Place` object, given its `id`"""
    place = [p for p in storage.all(Place).values() if p.id == place_id]
    if place:
        storage.delete(place[0])
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['PUT'])
def update_place(place_id):
    """Update a `Place` object, given its `id`"""
    place = [v for v in storage.all(Place).values() if v.id == place_id]
    if place:
        data = request.get_json()
        if not data:
            abort(400, description="Not a JSON")
        for key, value in data.items():
            if key not in ("id", "user_id", "email",
                           "created_at", "updated_at"):
                setattr(place[0], key, value)
#       state[0].__dict__.update(data)
        place[0].save()
        return jsonify(place[0].to_dict()), 200
    abort(404)


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['POST'])
def create_place(city_id):
    """Create a `Place` object"""
    data = request.get_json()
    city = [c for c in storage.all(City).values() if c.id == city_id]
    if city:
        if not data:
            abort(400, description="Not a JSON")
        user = [u for u in storage.all(User).values() if u.id == user_id]
        if not user:
            abort(404)
        if "user_id" not in data:
            abort(400, description="Missing user_id")
        if "name" not in data:
            abort(400, description="Missing name")
        place_obj = Place(**data)
        place_obj.save()
        return jsonify(place_obj.to_dict()), 201
    abort(404)


@app_views.errorhandler(404)
def not_found(error):
    """Handling not found error"""
    return jsonify({"error": "Not found"}), 404

#!/usr/bin/python3
"""Defines a view for `Amenity` objects"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def get_amenities():
    """Retrieve the list of `Amenity` objects"""
    amenity_dict = storage.all(Amenity)
    amenity_list = []
    for v in amenity_dict.values():
        amenity_list.append(v.to_dict())
    return jsonify(amenity_list)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET'])
def get_amenity(amenity_id):
    """Retrieve an `Amenity` object, given its `id`"""
    amenity = [v for v in storage.all(Amenity).values() if v.id == amenity_id]
    if amenity:
        amenity_dict = amenity[0].to_dict()
        return jsonify(amenity_dict)
    abort(404)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_amenity(amenity_id):
    """Delete an `Amenity` object, given its `id`"""
    amenity = [v for v in storage.all(Amenity).values() if v.id == amenity_id]
    if amenity:
        storage.delete(amenity[0])
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['PUT'])
def update_amenity(amenity_id):
    """Update an `Amenity` object, given its `id`"""
    amenity = [v for v in storage.all(Amenity).values() if v.id == amenity_id]
    if amenity:
        data = request.get_json()
        if not data:
            abort(400, description="Not a JSON")
        for key, value in data.items():
            if key not in ("id", "created_at", "uppdated_at"):
                setattr(amenity[0], key, value)
#       state[0].__dict__.update(data)
        amenity[0].save()
        return jsonify(amenity[0].to_dict()), 200
    abort(404)


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def create_amenity():
    """Create an `Amenity` object"""
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if "name" not in data:
        abort(400, description="Missing name")
    amenity_obj = Amenity(**data)
    amenity_obj.save()
    return jsonify(amenity_obj.to_dict()), 201


@app_views.errorhandler(404)
def not_found(error):
    """Handling not found error"""
    return jsonify({"error": "Not found"}), 404

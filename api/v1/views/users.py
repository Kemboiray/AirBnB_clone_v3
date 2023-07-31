#!/usr/bin/python3
"""Defines a view for `User` objects"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User
from models import storage


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def get_users():
    """Retrieve the list of `User` objects"""
    user_dict = storage.all(User)
    user_list = []
    for v in user_dict.values():
        user_list.append(v.to_dict())
    return jsonify(user_list)


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['GET'])
def get_user(user_id):
    """Retrieve a `User` object, given its `id`"""
    user = [v for v in storage.all(User).values() if v.id == user_id]
    if user:
        user_dict = user[0].to_dict()
        return jsonify(user_dict)
    abort(404)


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_user(user_id):
    """Delete a `User` object, given its `id`"""
    user = [v for v in storage.all(User).values() if v.id == user_id]
    if user:
        storage.delete(user[0])
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['PUT'])
def update_user(user_id):
    """Update a `user` object, given its `id`"""
    user = [v for v in storage.all(User).values() if v.id == user_id]
    if user:
        data = request.get_json()
        if not data:
            abort(400, description="Not a JSON")
        for key, value in data.items():
            if key not in ("id", "email", "created_at", "uppdated_at"):
                setattr(user[0], key, value)
#       state[0].__dict__.update(data)
        user[0].save()
        return jsonify(user[0].to_dict()), 200
    abort(404)


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def create_user():
    """Create a `User` object"""
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if "email" not in data:
        abort(400, description="Missing email")
    if "password" not in data:
        abort(400, description="Missing password")
    user_obj = User(**data)
    user_obj.save()
    return jsonify(user_obj.to_dict()), 201


@app_views.errorhandler(404)
def not_found(error):
    """Handling not found error"""
    return jsonify({"error": "Not found"}), 404

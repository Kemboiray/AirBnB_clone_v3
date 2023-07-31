#!/usr/bin/python3
"""Defines a view for `State` objects"""

from api.v1.views import app_views
from flask import jsonify, abort
from models.state import State
from models import storage


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def get_states():
    """Retrieve the list of `State` objects"""
    state_dict = storage.all(State)
    state_list = []
    for v in state_dict.values():
        state_list.append(v.to_dict())
    return jsonify(state_list)


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['GET'])
def get_state(state_id):
    """Retrieve a `State` object, given its `id`"""
    state = [v for v in storage.all(State).values() if v.id == state_id]
    if state:
        state_dict = state[0].to_dict()
        return jsonify(state_dict)
    abort(404)


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_state(state_id):
    """Delete a `State` object, given its `id`"""
    state = [v for v in storage.all(State).values() if v.id == state_id]
    if state:
        storage.delete(state[0])
        return jsonify({}), 200
    abort(404)


@app_views.errorhandler(404)
def not_found(error):
    """Handling not found error"""
    return jsonify({"error": "Not found"}), 404

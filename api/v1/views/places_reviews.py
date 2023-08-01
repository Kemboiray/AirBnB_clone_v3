#!/usr/bin/python3
"""Defines a view for `Review` objects"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.place import Place
from models.review import Review
from models.user import User
from models import storage


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['GET'])
def get_reviews(place_id):
    """Retrieve the list of `Review` objects subclassing a `Place` object"""
    place = [p for p in storage.all(Place).values() if p.id == place_id]
    if not place:
        abort(404)
    review_list = [r.to_dict() for r in storage.all(Review).values()
                   if r.place_id == place_id]
    return jsonify(review_list)


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=['GET'])
def get_review(review_id):
    """Retrieve a `Review` object"""
    review = [r for r in storage.all(Review).values() if r.id == review_id]
    if not review:
        abort(404)
    return jsonify(review[0].to_dict())


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_review(review_id):
    """Delete a `Review` object, given its `id`"""
    review = [r for r in storage.all(Review).values() if r.id == review_id]
    if review:
        storage.delete(review[0])
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['POST'])
def create_review(place_id):
    """Create a `Review` object"""
    place = [p for p in storage.all(Place).values() if p.id == place_id]
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if "user_id" not in data:
        abort(400, description="Missing user_id")
    user = [u for u in storage.all(User).values() if u.id == data["user_id"]]
    if not user:
        abort(404)
    if "text" not in data:
        abort(400, description="Missing text")
    data["place_id"] = place_id
    review_obj = Review(**data)
    review_obj.save()
    return jsonify(review_obj.to_dict()), 201


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['PUT'])
def update_review(review_id):
    """Update a `Review` object, given its `id`"""
    review = [r for r in storage.all(Review).values() if r.id == review_id]
    if review:
        data = request.get_json()
        if not data:
            abort(400, description="Not a JSON")
        for key, value in data.items():
            if key not in ("id", "user_id", "place_id", "created_at",
                           "uppdated_at"):
                setattr(review[0], key, value)
        review[0].save()
        return jsonify(review[0].to_dict()), 200
    abort(404)


@app_views.errorhandler(404)
def not_found(error):
    """Handling not found error"""
    return jsonify({"error": "Not found"}), 404

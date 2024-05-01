#!/usr/bin/python3
"""Amenity module for API"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Method to get the amenities"""
    amenities = storage.all(Amenity).values()
    if amenities is None:
        abort(404)
    amenity_list = []
    for amenity in amenities:
        amenity_list.append(amenity.to_dict())
    return jsonify(amenity_list), 200


@app_views.route('amenities/<amenity_id>', methods=['GET'])
def get_amenities_with_id(amenity_id):
    """Method to get amenity of a specific is"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict()), 200


@app_views.route('amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """ Method to delten amainity of the give ID"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    """Method to create a new amenity"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    new_amenity = Amenity(**request.get_json())
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """Method to update an amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200

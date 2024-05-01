#!/usr/bin/python3
"""Places module for the API"""
from models import storage
from models.place import Place
from models.city import City
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/places', methods=['GET'], strict_slashes=False)
def get_places():
    """Returns all places"""
    places = storage.all(Place).values()
    list_places = []
    for place in places:
        list_places.append(place.to_dict())
    return jsonify(list_places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place_id(place_id):
    """Returns a place by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a place of the given id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def post_place(city_id):
    """creates a new place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in request.get_json():
        return jsonify({"error": "Missing user_id"}), 400
    if 'name' not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    new_place = Place(**request.get_json())
    new_place.city_id = city_id
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """Updates a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in request.get_json().items():
        if key not in ['id', 'user_id', 'city_id', 'created', 'updated']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict())

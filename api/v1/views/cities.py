#!/usr/bin/python3
"""Get citites"""
from flask import jsonify, abort, request
from models.state import State
from models.city import City
from models import storage
from api.v1.views import app_views

@app_views.route('states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """Method to get a city linked to a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = []
    for city in state.cities:
        cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route('cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """Get city of the given id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Method to delete a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('states/<state_id>/cities', methods=['POST'])
def post_city(state_id):
    """Method to post a city"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    data = request.get_json()
    data['state_id'] = state_id
    city = City(**data)
    city.save()
    return city.to_dict(), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """Updates a state"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in request.get_json().items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200

 
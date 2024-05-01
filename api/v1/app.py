#!/usr/bin/python3
"""Main file for the API"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)

host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5000)


@app.teardown_appcontext
def close_db(exception=None):
    """method that closed db session"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """method that handles 404 errors"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True, debug=True)

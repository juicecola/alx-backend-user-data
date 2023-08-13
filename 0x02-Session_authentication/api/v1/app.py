#!/usr/bin/env python3
"""
API Route Configuration Module
"""

from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import CORS, cross_origin
import os

# Initialize the Flask app
app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None

# Get the authentication type from environment variable
AUTH_TYPE = os.getenv("AUTH_TYPE")

# Set up authentication based on AUTH_TYPE
if AUTH_TYPE == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()
elif AUTH_TYPE == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif AUTH_TYPE == 'session_auth':
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()

# Define a before_request handler to perform authentication and authorization
@app.before_request
def before_request():
    if auth is None:
        pass
    else:
        setattr(request, "current_user", auth.current_user(request))
        excluded_list = ['/api/v1/status/',
                         '/api/v1/unauthorized/', '/api/v1/forbidden/',
                         '/api/v1/auth_session/login/']

        if auth.require_auth(request.path, excluded_list):
            cookie = auth.session_cookie(request)
            if auth.authorization_header(request) is None and cookie is None:
                abort(401, description="Unauthorized")
            if auth.current_user(request) is None:
                abort(403, description='Forbidden')

# Define error handlers for different HTTP status codes
@app.errorhandler(404)
def not_found(error) -> str:
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(401)
def unauthorized(error) -> str:
    return jsonify({"error": "Unauthorized"}), 401

@app.errorhandler(403)
def forbidden(error) -> str:
    return jsonify({"error": "Forbidden"}), 403

# Run the app if executed directly
if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)


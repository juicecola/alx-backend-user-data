#!/usr/bin/env python3
"""
Flask app for user authentication and profile management.
"""

from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

AUTH = Auth()

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index() -> str:
    """
    Default route that returns a welcome message in JSON format.
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users() -> str:
    """
    Route to register a new user.

    Returns:
        JSON: A message indicating successful user registration or failure.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login() -> str:
    """
    Route to perform user login and create a session.

    Returns:
        JSON: A message indicating successful login or failure.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not AUTH.valid_login(email, password):
        abort(401)
    else:
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie('session_id', session_id)

    return response


@app.route('/sessions', methods=['DELETE'])
def logout() -> str:
    """
    Route to logout a user and destroy the session.

    Returns:
        Redirect: Redirects to the root URL.
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')

# ... (Other routes follow with similar detailed comments)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

#!/usr/bin/env python3
"""
Module for User views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User

# Route to get all users
@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """ GET /api/v1/users
    Returns:
        str: JSON representation of a list of all User objects
    """
    all_users = [user.to_json() for user in User.all()]
    return jsonify(all_users)

# Route to get a specific user
@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    """ GET /api/v1/users/:id
    Args:
        user_id (str): Path parameter for User ID
    Returns:
        str: JSON representation of a User object
            404 if User ID doesn't exist
    """
    if user_id is None:
        abort(404)
    if user_id == "me":
        if request.current_user is None:
            abort(404)
        user = request.current_user
        return jsonify(user.to_json())
    user = User.get(user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_json())

# Route to delete a user
@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    """ DELETE /api/v1/users/:id
    Args:
        user_id (str): Path parameter for User ID
    Returns:
        str: Empty JSON if User has been deleted, 404 if User ID doesn't exist
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    user.remove()
    return jsonify({}), 200

# Route to create a new user
@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """ POST /api/v1/users/
    Returns:
        str: JSON representation of a User object
            400 if unable to create the new User
    """
    rj = None
    error_msg = None
    try:
        rj = request.get_json()
    except Exception as e:
        rj = None
    if rj is None:
        error_msg = "Wrong format"
    if error_msg is None and rj.get("email", "") == "":
        error_msg = "email missing"
    if error_msg is None and rj.get("password", "") == "":
        error_msg = "password missing"
    if error_msg is None:
        try:
            user = User()
            user.email = rj.get("email")
            user.password = rj.get("password")
            user.first_name = rj.get("first_name")
            user.last_name = rj.get("last_name")
            user.save()
            return jsonify(user.to_json()), 201
        except Exception as e:
            error_msg = "Can't create User: {}".format(e)
    return jsonify({'error': error_msg}), 400

# Route to update an existing user
@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str = None) -> str:
    """ PUT /api/v1/users/:id
    Args:
        user_id (str): Path parameter for User ID
    Returns:
        str: JSON representation of an updated User object
            404 if User ID doesn't exist
            400 if unable to update the User
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    rj = None
    try:
        rj = request.get_json()
    except Exception as e:
        rj = None
    if rj is None:
        return jsonify({'error': "Wrong format"}), 400
    if rj.get('first_name') is not None:
        user.first_name = rj.get('first_name')
    if rj.get('last_name') is not None:
        user.last_name = rj.get('last_name')
    user.save()
    return jsonify(user.to_json()), 200


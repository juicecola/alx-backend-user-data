#!/usr/bin/env python3
""" Module for defining API views and routes.
"""
from flask import Blueprint
from models.user import User

# Create a Blueprint for the API views with a URL prefix
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Import specific view modules to include their routes
from api.v1.views.index import *
from api.v1.views.users import *
from api.v1.views.session_auth import *

# Load user data from a file
User.load_from_file()


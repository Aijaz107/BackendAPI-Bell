"""
User Management Routes Module

This module defines all RESTful API endpoints for user management operations.
Implements CRUD (Create, Read, Update, Delete) operations for user accounts.

Endpoints:
    GET    /api/users/          - Retrieve all users
    GET    /api/users/<id>      - Retrieve a specific user by ID
    POST   /api/users/          - Create a new user
    PUT    /api/users/<id>      - Update an existing user
    DELETE /api/users/<id>      - Delete a user

Author: Backend API Team
Version: 1.0.0
"""

from flask import Blueprint, request, jsonify
from ..models import User
from .. import db
from ..services.user_service import (
    create_user_service,
    update_user_service,
    delete_user_service,
    get_all_users_service,
    get_user_service
)

# Create Blueprint for user management routes
users_bp = Blueprint("users", __name__)


@users_bp.route("/", methods=["GET"])
def get_all_users():
    """
    Retrieve all users from the database.
    
    Returns:
        tuple: JSON response containing list of users and HTTP status code
            - 200: Successfully retrieved users
            - Response format: [{"id": 1, "first_name": "...", ...}, ...]
    """
    return get_all_users_service()


@users_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id: int):
    """
    Retrieve a specific user by ID.
    
    Args:
        user_id (int): The unique identifier of the user to retrieve
    
    Returns:
        tuple: JSON response containing user data and HTTP status code
            - 200: User found and returned
            - 404: User not found
    """
    return get_user_service(user_id)


@users_bp.route("/", methods=["POST"])
def create_user():
    """
    Create a new user account.
    
    Expected request format (multipart/form-data):
        - first_name (str, required): User's first name
        - last_name (str, required): User's last name
        - email (str, required): User's email address
        - password (str, required): User's password
        - image (file, optional): Profile image (JPG, JPEG, PNG)
    
    Returns:
        tuple: JSON response containing created user data and HTTP status code
            - 201: User successfully created
            - 400: Missing required fields
    """
    return create_user_service(request)


@users_bp.route("/<int:user_id>", methods=["PUT"])
def update_user(user_id: int):
    """
    Update an existing user's information.
    
    Args:
        user_id (int): The unique identifier of the user to update
    
    Request format (multipart/form-data):
        - first_name (str, optional): Updated first name
        - last_name (str, optional): Updated last name
        - email (str, optional): Updated email address
        - password (str, optional): Updated password
        - image (file, optional): New profile image
    
    Returns:
        tuple: JSON response containing updated user data and HTTP status code
            - 200: User successfully updated
            - 404: User not found
    """
    return update_user_service(user_id, request)


@users_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id: int):
    """
    Delete a user account and associated files.
    
    This endpoint removes the user from the database and any associated
    profile images from the file system.
    
    Args:
        user_id (int): The unique identifier of the user to delete
    
    Returns:
        tuple: JSON response with status message and HTTP status code
            - 200: User successfully deleted
            - 404: User not found
    """
    return delete_user_service(user_id)

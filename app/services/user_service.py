"""
User Service Module

This module implements the business logic for user management operations.
It serves as an intermediary between API routes and the database layer,
handling validation, file operations, and data transformations.

Author: Backend API Team
Version: 1.0.0
"""

from flask import jsonify
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import User
from .. import db
import os

# Allowed file extensions for user profile images
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}


def allowed_file(filename: str) -> bool:
    """
    Validate if uploaded file has an allowed extension.
    
    This function checks if a file extension is in the whitelist of allowed
    image formats. Only security-approved image types are allowed.
    
    Args:
        filename (str): The name of the file to validate
        
    Returns:
        bool: True if file has an allowed extension, False otherwise
        
    Example:
        >>> allowed_file("profile.jpg")
        True
        >>> allowed_file("script.exe")
        False
    """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_all_users_service():
    """
    Retrieve all users from the database.
    
    Fetches all user records and returns them as a JSON array.
    Note: Passwords are not included in the response for security.
    
    Returns:
        tuple: (JSON response, HTTP status code)
            - JSON: List of user dictionaries
            - Status: 200 (OK)
    """
    # Query all users from database
    users = User.query.all()
    users_list = []
    
    # Build list of user dictionaries, excluding sensitive data
    for user in users:
        users_list.append({
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'image': user.image  # Only send filename, not full path
        })
    
    return jsonify(users_list), 200


def get_user_service(user_id: int):
    """
    Retrieve a specific user by ID.
    
    Fetches a single user record from the database and returns it as JSON.
    Returns 404 error if user is not found.
    
    Args:
        user_id (int): The unique identifier of the user to retrieve
        
    Returns:
        tuple: (JSON response, HTTP status code)
            - 200: User found, returns user data
            - 404: User not found
    """
    # Query for user by primary key
    user = User.query.get(user_id)

    # Handle not found case
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Return user data converted to dictionary
    return jsonify(user.to_dict()), 200


def create_user_service(request):
    """
    Create a new user account.
    
    Validates required fields, handles optional image upload, and creates
    a new user record in the database.
    
    Args:
        request: Flask request object containing form data and files
        
    Returns:
        tuple: (JSON response, HTTP status code)
            - 201: User successfully created
            - 400: Missing required fields
            
    Expected form data:
        - first_name (str): User's first name
        - last_name (str): User's last name
        - email (str): User's email
        - password (str): User's password (should be hashed in production)
        - image (file, optional): Profile image file
    """
    # Extract form data from request
    data = request.form

    # Define required fields for user creation
    required_fields = ["first_name", "last_name", "email", "password"]
    
    # Check for missing required fields
    missing = [field for field in required_fields if not data.get(field)]

    if missing:
        return jsonify({
            "error": f"Missing fields: {', '.join(missing)}"
        }), 400

    # Handle optional image upload
    image_file = request.files.get("image")

    filename = None
    if image_file and allowed_file(image_file.filename):
        # Secure the filename to prevent directory traversal attacks
        filename = secure_filename(image_file.filename)
        upload_path = os.path.join("uploads/photos", filename)
        image_file.save(upload_path)

    # Create new user instance with provided data
    user = User(
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
        password=generate_password_hash(data["password"]),
        image=filename
    )

    # Add user to session and commit to database
    db.session.add(user)
    db.session.commit()

    # Return created user data with 201 status (Created)
    return jsonify(user.to_dict()), 201


def update_user_service(user_id: int, request):
    """
    Update an existing user's information.
    
    Finds the user by ID and updates specified fields. Unspecified fields
    retain their original values. Handles optional image file updates.
    
    Args:
        user_id (int): The unique identifier of the user to update
        request: Flask request object containing form data and files
        
    Returns:
        tuple: (JSON response, HTTP status code)
            - 200: User successfully updated
            - 404: User not found
            
    Optional fields:
        - first_name (str): Updated first name
        - last_name (str): Updated last name
        - email (str): Updated email
        - password (str): Updated password
        - image (file): New profile image
    """
    # Query for user by ID
    user = User.query.get(user_id)

    # Handle not found case
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Extract form data from request
    data = request.form

    # Update fields if provided, otherwise keep existing values
    user.first_name = data.get("first_name", user.first_name)
    user.last_name = data.get("last_name", user.last_name)
    user.email = data.get("email", user.email)
    # Only update password if provided; store as a hash
    if data.get("password"):
        user.password = generate_password_hash(data.get("password"))

    # Handle optional image update
    image_file = request.files.get("image")
    if image_file and allowed_file(image_file.filename):
        filename = secure_filename(image_file.filename)
        upload_path = os.path.join("uploads/photos", filename)
        image_file.save(upload_path)
        user.image = filename

    # Commit changes to database
    db.session.commit()

    # Return updated user data
    return jsonify(user.to_dict()), 200


def verify_user_password(user: User, plain_password: str) -> bool:
    """
    Verify a plaintext password against the stored hash.

    Args:
        user (User): User model instance with `password` hash
        plain_password (str): Plaintext password to verify

    Returns:
        bool: True if password matches, False otherwise
    """
    return check_password_hash(user.password, plain_password)


def delete_user_service(user_id: int):
    """
    Delete a user account and associated files.
    
    Removes the user record from the database and deletes any associated
    profile image files from the file system.
    
    Args:
        user_id (int): The unique identifier of the user to delete
        
    Returns:
        tuple: (JSON response, HTTP status code)
            - 200: User successfully deleted
            - 404: User not found
    """
    # Query for user by ID
    user = User.query.get(user_id)

    # Handle not found case
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Delete associated image file if it exists
    if user.image:
        image_path = os.path.join("uploads/photos", user.image)
        if os.path.exists(image_path):
            os.remove(image_path)

    # Remove user from database and commit changes
    db.session.delete(user)
    db.session.commit()

    # Return success message
    return jsonify({"message": "User deleted successfully"}), 200


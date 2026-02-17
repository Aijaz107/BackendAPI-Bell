"""
Database Models Module

This module defines the SQLAlchemy ORM models for the application.
Currently contains the User model for user management.

Author: Backend API Team
Version: 1.0.0
"""

from . import db


class User(db.Model):
    """
    User database model for storing user account information.
    
    This model represents a user in the system with basic profile information
    and authentication credentials. Each user has a unique email address.
    
    Attributes:
        id (int): Primary key, auto-incremented user identifier
        first_name (str): User's first name (max 100 characters)
        last_name (str): User's last name (max 100 characters)
        email (str): User's email address (must be unique)
        password (str): User's password (hashed in production)
        image (str): Filename of user's profile image (optional)
    
    Example:
        user = User(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            password="hashed_password",
            image="profile.jpg"
        )
        db.session.add(user)
        db.session.commit()
    """
    
    __tablename__ = "users"

    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # User profile information (required fields)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    
    # Email must be unique across all users for identification
    email = db.Column(db.String(100), unique=True, nullable=False)
    
    # Password field (stored as a hash)
    # Increase column length to accommodate hashed values
    password = db.Column(db.String(1000), nullable=False)
    
    # Optional profile image filename
    image = db.Column(db.String(200))

    def to_dict(self) -> dict:
        """
        Convert user object to dictionary representation.
        
        This method is used for JSON serialization in API responses.
        Note: Password is intentionally excluded for security reasons.
        
        Returns:
            dict: Dictionary containing user data
                - id: User identifier
                - first_name: User's first name
                - last_name: User's last name
                - email: User's email address
                - image: User's profile image filename or None
        """
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "image": self.image
        }

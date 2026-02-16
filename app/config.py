"""
Application Configuration Module

This module contains environment-based configuration settings for the Flask application.
It manages database connections, security keys, and file upload settings.

Configuration can be overridden using environment variables for secure credential management.

Author: Backend API Team
Version: 1.0.0
"""

import os


class Config:
    """
    Configuration class for Flask application.
    
    This class centralizes all application configuration settings including:
    - Database connection parameters
    - Security settings
    - File upload configurations
    
    Environment Variables:
        SECRET_KEY: Secret key for session encryption (default: dev-secret-key)
        DATABASE_URL: Database connection URI (default: MySQL on localhost)
    """
    
    # Secret key for session management and CSRF protection
    # NOTE: Change this in production! Use a secure, random value.
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    
    # Database connection URI
    # Currently configured for MySQL, but can be changed for other databases
    # Format: dialect+driver://user:password@host:port/database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "mysql://myadmin:123456@localhost:3306/flask_crud"
    )
    
    # Disable modification tracking to improve performance
    # Warning: Set to False in production after verifying all models
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Directory path for storing uploaded user files (e.g., profile images)
    UPLOAD_FOLDER = "uploads/photos"

"""
Application Factory Module

This module contains the Flask application factory function and database initialization.
It is responsible for creating and configuring the Flask application instance with all
required extensions, blueprints, and middleware.

Author: Backend API Team
Version: 1.0.0
"""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .config import Config

# Initialize SQLAlchemy ORM for database operations
db = SQLAlchemy()


def create_app() -> Flask:
    """
    Application factory function that creates and configures the Flask application.
    
    This function initializes the Flask application with the following components:
    - Database configuration and initialization
    - CORS (Cross-Origin Resource Sharing) support
    - Static file serving for uploads
    - API blueprints and routes
    
    Returns:
        Flask: Configured Flask application instance ready for running.
        
    Raises:
        OSError: If upload directory cannot be created.
    """
    # Get the base directory path (project root)
    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    # Define uploads directory path for storing user-uploaded files
    uploads_path = os.path.join(base_dir, 'uploads')

    # Create Flask app instance with static file configuration
    app = Flask(
        __name__,
        static_url_path='/uploads',
        static_folder=uploads_path
    )

    # Configure upload folder for user profile images
    app.config['UPLOAD_FOLDER'] = 'uploads/photos'
    
    # Create uploads directory if it doesn't exist
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    # Load configuration from Config class
    app.config.from_object(Config)

    # Enable CORS for all routes to allow cross-origin requests
    CORS(app)
    
    # Initialize database with Flask app
    db.init_app(app)

    # Register user management blueprint
    from .routes.users import users_bp
    app.register_blueprint(users_bp, url_prefix="/api/users")

    return app

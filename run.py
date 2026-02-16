"""
Application Entry Point

This module serves as the main entry point for running the Flask development server.
It initializes the application, creates database tables, and starts the server.

Usage:
    python run.py

The application will start on http://localhost:5000 with debug mode enabled.

Author: Backend API Team
Version: 1.0.0
"""

from app import create_app, db

# Create and configure the Flask application
app = create_app()

if __name__ == "__main__":
    # Create database tables within application context
    with app.app_context():
        # Initialize database tables from model definitions
        db.create_all()
    
    # Start the Flask development server with debug mode enabled
    # Debug mode provides auto-reloading and interactive debugger
    app.run(debug=True)

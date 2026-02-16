import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .config import Config

db = SQLAlchemy()

def create_app():
    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    uploads_path = os.path.join(base_dir, 'uploads')

    app = Flask(
        __name__,
        static_url_path='/uploads',
        static_folder=uploads_path
    )


    app.config['UPLOAD_FOLDER'] = 'uploads/photos'
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)

    from .routes.users import users_bp
    app.register_blueprint(users_bp, url_prefix="/api/users")

    return app

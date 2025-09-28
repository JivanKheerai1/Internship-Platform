import os
from flask import Flask, render_template
from flask_cors import CORS
from flask_uploads import DOCUMENTS, IMAGES, TEXT, UploadSet, configure_uploads
from dotenv import load_dotenv

from App.database import db, migrate, init_db
from App.config import load_config
from App.controllers import setup_jwt, add_auth_context
from App.views import user_views, admin_views  # import your blueprints here

load_dotenv()  # load environment variables from .env

def create_app(overrides={}):
    # Initialize Flask app
    app = Flask(__name__, static_url_path='/static')

    # Load config from .env
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///temp-database.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "devkey")

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # Register blueprints
    app.register_blueprint(user_views)
    app.register_blueprint(admin_views)

    # Additional setup
    add_auth_context(app)
    load_config(app, overrides)

    # File uploads
    photos = UploadSet('photos', TEXT + DOCUMENTS + IMAGES)
    configure_uploads(app, photos)

    # Initialize database
    init_db(app)

    # JWT setup
    jwt = setup_jwt(app)

    @jwt.invalid_token_loader
    @jwt.unauthorized_loader
    def custom_unauthorized_response(error):
        return render_template('401.html', error=error), 401

    return app

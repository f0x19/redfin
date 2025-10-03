import os
from flask import Flask
from dotenv import load_dotenv

from .config import Config
from .extensions import db, migrate


def create_app() -> Flask:
    """Application factory for the real estate app."""
    # Load environment variables from .env if present
    load_dotenv()

    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(Config())

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from .routes.pages import pages_bp
    from .routes.properties import api_bp

    app.register_blueprint(pages_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    # Register CLI commands
    from .cli import register_cli

    register_cli(app)

    return app

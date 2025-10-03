from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os import getenv
from dotenv import load_dotenv
import os

# Initialize extensions

db = SQLAlchemy()
migrate = Migrate()


def create_app(test_config: dict | None = None) -> Flask:
    """Application factory for the Redfin-like real estate site."""
    load_dotenv()

    app = Flask(__name__, instance_relative_config=True)

    # Default configuration
    app.config.from_mapping(
        SECRET_KEY=getenv("SECRET_KEY", "dev-secret-key"),
        SQLALCHEMY_DATABASE_URI=getenv(
            "DATABASE_URL",
            # Example: mysql://user:pass@localhost:3306/realestate
            "mysql+pymysql://root:password@localhost:3306/realestate",
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JSON_SORT_KEYS=False,
        PER_PAGE=int(getenv("PER_PAGE", "12")),
    )

    if test_config is not None:
        app.config.update(test_config)

    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    # CLI commands
    from . import cli as cli_commands
    cli_commands.init_app(app)

    return app

import os
from urllib.parse import quote_plus


class Config:
    """Base configuration loaded into the Flask app."""

    # Flask
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")

    # Pagination
    PER_PAGE = int(os.getenv("PER_PAGE", "12"))

    # SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO", "false").lower() == "true"

    # Database URL resolution
    _database_url = os.getenv("DATABASE_URL")

    if not _database_url:
        mysql_host = os.getenv("MYSQL_HOST")
        mysql_port = os.getenv("MYSQL_PORT", "3306")
        mysql_user = os.getenv("MYSQL_USER")
        mysql_password = os.getenv("MYSQL_PASSWORD")
        mysql_db = os.getenv("MYSQL_DB") or os.getenv("MYSQL_DATABASE")

        if mysql_host and mysql_user and mysql_password and mysql_db:
            # URL-encode password in case it has special characters
            safe_password = quote_plus(mysql_password)
            _database_url = (
                f"mysql+pymysql://{mysql_user}:{safe_password}@{mysql_host}:{mysql_port}/{mysql_db}"
            )

    # Fallback to sqlite for local dev if MySQL is not configured
    if not _database_url:
        # Use absolute path for SQLite to avoid cwd-related issues
        project_root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        instance_dir = os.path.join(project_root, "instance")
        os.makedirs(instance_dir, exist_ok=True)
        sqlite_path = os.path.join(instance_dir, "app.db")
        _database_url = f"sqlite:///{sqlite_path}"

    SQLALCHEMY_DATABASE_URI = _database_url

    # Engine options
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

"""Configuration objects, one per environment.

Secrets and connection strings are read from the environment (loaded from a
`.env` file) so nothing sensitive is hard-coded (see dev-principles on secrets).
"""
import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")


def _default_sqlite_uri() -> str:
    return "sqlite:///" + os.path.join(INSTANCE_DIR, "ppa.db").replace("\\", "/")


class BaseConfig:
    """Settings shared by every environment."""

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-in-production-0123456789")
    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY", "dev-jwt-secret-change-in-production-0123456789"
    )
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=12)

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or _default_sqlite_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Caching (Redis). CACHE_DEFAULT_TIMEOUT is the fallback expiry in seconds.
    CACHE_TYPE = os.getenv("CACHE_TYPE", "RedisCache")
    CACHE_REDIS_URL = os.getenv("CACHE_REDIS_URL", "redis://localhost:6379/1")
    CACHE_DEFAULT_TIMEOUT = 60

    # Celery broker / result backend.
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # Pre-seeded admin.
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@ppa.local")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

    # Email.
    MAIL_BACKEND = os.getenv("MAIL_BACKEND", "console")
    MAIL_FROM = os.getenv("MAIL_FROM", "placement-cell@ppa.local")
    SMTP_HOST = os.getenv("SMTP_HOST", "")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")

    # Filesystem locations for uploaded resumes and generated CSV exports.
    UPLOAD_FOLDER = os.path.join(INSTANCE_DIR, "uploads")
    EXPORT_FOLDER = os.path.join(INSTANCE_DIR, "exports")
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB cap on uploads

    REMINDER_DEADLINE_DAYS = int(os.getenv("REMINDER_DEADLINE_DAYS", "3"))


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    CACHE_TYPE = "SimpleCache"


_CONFIGS = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}


def get_config(name: str | None = None):
    """Return the config class for `name` (falls back to FLASK_ENV)."""
    resolved = name or os.getenv("FLASK_ENV", "development")
    return _CONFIGS.get(resolved, DevelopmentConfig)

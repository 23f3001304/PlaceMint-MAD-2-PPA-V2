"""Application factory.

`create_app()` wires config, extensions, models, blueprints and error handlers,
then creates the SQLite schema and seeds the single admin account.
"""
import os

from flask import Flask

from app.config import get_config
from app.extensions import cache, db, jwt


def create_app(config_name: str | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(get_config(config_name))

    _ensure_runtime_dirs(app)

    db.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)

    from app import models  # noqa: F401  (imported so all tables register)

    from app.tasks import make_celery

    make_celery(app)

    from app.api import register_api
    from app.api.errors import register_error_handlers
    from app.auth.tokens import register_jwt_handlers

    register_jwt_handlers(jwt)
    register_api(app)
    register_error_handlers(app)
    _register_security_headers(app)

    _init_database(app)
    return app


def _register_security_headers(app: Flask) -> None:
    @app.after_request
    def _headers(response):
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "no-referrer")
        response.headers.setdefault(
            "Content-Security-Policy",
            "default-src 'self'; img-src 'self' data: https:; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com; script-src 'self'; "
            "object-src 'none'; frame-ancestors 'none'",
        )
        return response


def _ensure_runtime_dirs(app: Flask) -> None:
    """Create instance/, uploads/ and exports/ before the DB file is opened."""
    for key in ("UPLOAD_FOLDER", "EXPORT_FOLDER"):
        os.makedirs(app.config[key], exist_ok=True)


def _init_database(app: Flask) -> None:
    with app.app_context():
        db.create_all()
        from app.seed import seed_admin

        seed_admin()

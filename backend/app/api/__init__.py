"""Register every API blueprint under /api.

Blueprints are added here as each feature phase lands; keeping registration in
one place makes the app's surface easy to scan.
"""


def register_api(app):
    from app.api.auth.routes import auth_bp
    from app.api.health import health_bp

    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

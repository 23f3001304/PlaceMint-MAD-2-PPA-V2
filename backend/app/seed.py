"""Seed the single admin account programmatically after schema creation.

The spec forbids admin registration, so the admin exists only because this
runs at startup. It is idempotent; a second run is a no-op.
"""
from flask import current_app

from app.auth.passwords import hash_password
from app.extensions import db
from app.models.constants import Role
from app.models.user import User


def seed_admin() -> None:
    if User.query.filter_by(role=Role.ADMIN).first():
        return

    admin = User(
        email=current_app.config["ADMIN_EMAIL"],
        password_hash=hash_password(current_app.config["ADMIN_PASSWORD"]),
        role=Role.ADMIN,
    )
    db.session.add(admin)
    db.session.commit()
    current_app.logger.info("Seeded admin account: %s", admin.email)

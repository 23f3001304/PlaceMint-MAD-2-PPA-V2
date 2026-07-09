"""Shareable, read-only profile pages for students and companies."""
from flask import Blueprint

directory_bp = Blueprint("directory", __name__)

from app.api.directory import profiles  # noqa: E402,F401  (attaches routes)

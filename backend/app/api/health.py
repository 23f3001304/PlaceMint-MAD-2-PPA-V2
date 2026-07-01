"""Liveness probe used by the verification walkthrough and uptime checks."""
from flask import Blueprint

from app.utils.responses import ok

health_bp = Blueprint("health", __name__)


@health_bp.get("/health")
def health():
    return ok({"status": "healthy", "service": "placement-portal"})

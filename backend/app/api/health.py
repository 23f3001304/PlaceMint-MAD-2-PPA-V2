"""Public endpoints: liveness probe and pre-login aggregate statistics."""
from flask import Blueprint

from app.services.stats.admin_stats import chart_data, dashboard_counts
from app.utils.responses import ok

health_bp = Blueprint("health", __name__)


@health_bp.get("/health")
def health():
    return ok({"status": "healthy", "service": "placement-portal"})


@health_bp.get("/public/stats")
def public_stats():
    """Read-only aggregates for the landing page (no sensitive data)."""
    counts = dashboard_counts()
    charts = chart_data()
    return ok({
        "students": counts["students"],
        "companies": counts["companies"],
        "drives": counts["drives"],
        "applications": counts["applications"],
        "placements": counts["placements"],
        "applications_by_status": charts["applications_by_status"],
        "students_by_branch": charts["students_by_branch"],
    })

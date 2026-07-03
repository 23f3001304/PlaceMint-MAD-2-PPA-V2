"""Admin dashboard counts and chart aggregates."""
from flask import Blueprint

from app.auth.rbac import role_required
from app.caching.keys import STATS_TTL, admin_charts_key, admin_counts_key, get_or_set
from app.models.constants import Role
from app.services.stats.admin_stats import chart_data, dashboard_counts
from app.utils.responses import ok

admin_dash_bp = Blueprint("admin_dashboard", __name__)


@admin_dash_bp.get("/stats")
@role_required(Role.ADMIN)
def stats():
    return ok(get_or_set(admin_counts_key(), STATS_TTL, dashboard_counts))


@admin_dash_bp.get("/stats/charts")
@role_required(Role.ADMIN)
def charts():
    return ok(get_or_set(admin_charts_key(), STATS_TTL, chart_data))

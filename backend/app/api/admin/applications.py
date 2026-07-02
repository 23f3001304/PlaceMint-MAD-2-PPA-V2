"""Admin view of every application across the institute."""
from flask import Blueprint, request

from app.auth.rbac import role_required
from app.models.constants import ApplicationStatus, Role
from app.models.placement.application import Application
from app.utils.responses import ok, serve_page

admin_apps_bp = Blueprint("admin_applications", __name__)


@admin_apps_bp.get("")
@role_required(Role.ADMIN)
def list_applications():
    query = Application.query
    status = request.args.get("status")
    if status in ApplicationStatus.ALL:
        query = query.filter_by(status=status)
    return serve_page(
        query.order_by(Application.applied_at.desc()),
        lambda a: a.to_dict(include_drive=True, include_student=True),
    )

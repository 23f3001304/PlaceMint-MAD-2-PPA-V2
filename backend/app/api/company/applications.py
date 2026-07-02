"""Company applicant review: list per drive, update status/feedback/interview."""
from flask import Blueprint, request

from app.auth.rbac import current_company, role_required
from app.models.constants import Role
from app.services.applications.application_service import list_applicants, update_application
from app.services.drives.drive_service import get_owned_drive
from app.utils.responses import ok

company_apps_bp = Blueprint("company_applications", __name__)


@company_apps_bp.get("/drive/<int:drive_id>")
@role_required(Role.COMPANY)
def applicants(drive_id):
    drive = get_owned_drive(current_company(), drive_id)
    return ok(list_applicants(drive))


@company_apps_bp.patch("/<int:app_id>")
@role_required(Role.COMPANY)
def update(app_id):
    app = update_application(current_company(), app_id, request.get_json(silent=True) or {})
    return ok(app.to_dict(include_student=True))

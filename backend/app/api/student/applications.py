"""Student applications: apply to a drive, view history and placements."""
from flask import Blueprint, request

from app.auth.rbac import current_student, role_required
from app.models.constants import Role
from app.services.applications.application_service import apply
from app.utils.responses import created, ok

student_apps_bp = Blueprint("student_applications", __name__)


@student_apps_bp.post("")
@role_required(Role.STUDENT)
def create():
    drive_id = (request.get_json(silent=True) or {}).get("drive_id")
    application = apply(current_student(), drive_id)
    return created(application.to_dict(include_drive=True))


@student_apps_bp.get("")
@role_required(Role.STUDENT)
def history():
    apps = sorted(
        current_student().applications,
        key=lambda a: a.applied_at or a.id,
        reverse=True,
    )
    return ok([a.to_dict(include_drive=True) for a in apps])


@student_apps_bp.get("/placements")
@role_required(Role.STUDENT)
def placements():
    return ok([p.to_dict() for p in current_student().placements])

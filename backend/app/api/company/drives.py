"""Company drive management: list, create (post-approval), edit, open/close."""
from flask import Blueprint, request

from app.api.company.schema import clean_drive
from app.auth.rbac import approved_company, current_company, role_required
from app.models.constants import Role
from app.services.drives.drive_service import (
    company_set_status,
    create_drive,
    delete_drive,
    get_owned_drive,
    list_company_drives,
    update_drive,
)
from app.utils.responses import created, ok

company_drives_bp = Blueprint("company_drives", __name__)


@company_drives_bp.get("")
@role_required(Role.COMPANY)
def list_drives():
    return ok([d.to_dict() for d in list_company_drives(current_company().id)])


@company_drives_bp.post("")
@role_required(Role.COMPANY)
def create():
    company = approved_company()
    drive = create_drive(company, clean_drive(request.get_json(silent=True) or {}))
    return created(drive.to_dict())


@company_drives_bp.patch("/<int:drive_id>")
@role_required(Role.COMPANY)
def update(drive_id):
    company = approved_company()
    drive = update_drive(company, drive_id, clean_drive(request.get_json(silent=True) or {}))
    return ok(drive.to_dict())


@company_drives_bp.post("/<int:drive_id>/status")
@role_required(Role.COMPANY)
def set_status(drive_id):
    new_status = (request.get_json(silent=True) or {}).get("status")
    return ok(company_set_status(current_company(), drive_id, new_status).to_dict())


@company_drives_bp.delete("/<int:drive_id>")
@role_required(Role.COMPANY)
def remove(drive_id):
    drive = get_owned_drive(current_company(), drive_id)
    delete_drive(drive.id)
    return ok({"deleted": drive_id})

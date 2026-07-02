"""Admin drive oversight: list, approve/reject, close, delete."""
from flask import Blueprint, request

from app.auth.rbac import role_required
from app.models.constants import DriveStatus, Role
from app.models.placement.drive import PlacementDrive
from app.services.drives.drive_service import close_drive, delete_drive, set_drive_status
from app.utils.responses import ok, serve_page

admin_drives_bp = Blueprint("admin_drives", __name__)


@admin_drives_bp.get("")
@role_required(Role.ADMIN)
def list_drives():
    query = PlacementDrive.query
    status = request.args.get("status")
    if status in DriveStatus.ALL:
        query = query.filter_by(status=status)
    q = request.args.get("q", "").strip()
    if q:
        query = query.filter(PlacementDrive.job_title.ilike(f"%{q}%"))
    return serve_page(query.order_by(PlacementDrive.created_at.desc()), lambda d: d.to_dict())


@admin_drives_bp.post("/<int:drive_id>/approval")
@role_required(Role.ADMIN)
def approval(drive_id):
    status = (request.get_json(silent=True) or {}).get("status")
    return ok(set_drive_status(drive_id, status).to_dict())


@admin_drives_bp.post("/<int:drive_id>/close")
@role_required(Role.ADMIN)
def close(drive_id):
    return ok(close_drive(drive_id).to_dict())


@admin_drives_bp.delete("/<int:drive_id>")
@role_required(Role.ADMIN)
def remove(drive_id):
    delete_drive(drive_id)
    return ok({"deleted": drive_id})

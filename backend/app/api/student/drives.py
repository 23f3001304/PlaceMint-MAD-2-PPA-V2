"""Student browsing: eligible approved drives and the organizations behind them.

Only drives that are admin-approved and belong to an approved, active,
non-blacklisted company are ever visible here.
"""
from flask import Blueprint, request

from app.auth.rbac import current_student, role_required
from app.models.constants import ApprovalStatus, DriveStatus, Role
from app.models.placement.drive import PlacementDrive
from app.models.profiles.company import CompanyProfile
from app.models.user import User
from app.services.drives.eligibility import to_student_dict
from app.utils.errors import NotFoundError
from app.utils.responses import ok

student_drives_bp = Blueprint("student_drives", __name__)


def _visible_drives():
    return (
        PlacementDrive.query.join(CompanyProfile)
        .join(User, CompanyProfile.user_id == User.id)
        .filter(
            PlacementDrive.status == DriveStatus.APPROVED,
            CompanyProfile.approval_status == ApprovalStatus.APPROVED,
            User.is_active.is_(True),
            User.is_blacklisted.is_(False),
        )
    )


@student_drives_bp.get("")
@role_required(Role.STUDENT)
def list_drives():
    student = current_student()
    query = _visible_drives()
    if (q := request.args.get("q", "").strip()):
        query = query.filter(PlacementDrive.job_title.ilike(f"%{q}%"))
    if (company := request.args.get("company", "").strip()):
        query = query.filter(CompanyProfile.company_name.ilike(f"%{company}%"))
    skill = request.args.get("skill", "").strip().lower()
    eligible_only = request.args.get("eligible_only") == "true"
    applied_ids = {a.drive_id for a in student.applications}

    result = []
    for drive in query.order_by(PlacementDrive.deadline).all():
        if skill and skill not in [s.lower() for s in (drive.skills_required or [])]:
            continue
        item = to_student_dict(student, drive)
        if eligible_only and not item["eligible"]:
            continue
        item["applied"] = drive.id in applied_ids
        result.append(item)
    return ok(result)


@student_drives_bp.get("/<int:drive_id>")
@role_required(Role.STUDENT)
def drive_detail(drive_id):
    student = current_student()
    drive = _visible_drives().filter(PlacementDrive.id == drive_id).first()
    if drive is None:
        raise NotFoundError("Drive not found")
    item = to_student_dict(student, drive)
    item["applied"] = any(a.drive_id == drive.id for a in student.applications)
    return ok(item)


@student_drives_bp.get("/organizations")
@role_required(Role.STUDENT)
def organizations():
    query = CompanyProfile.query.filter_by(approval_status=ApprovalStatus.APPROVED)
    if (q := request.args.get("q", "").strip()):
        query = query.filter(CompanyProfile.company_name.ilike(f"%{q}%"))
    out = []
    for company in query.order_by(CompanyProfile.company_name).all():
        data = company.to_dict()
        data["open_drives"] = sum(1 for d in company.drives if d.status == DriveStatus.APPROVED)
        out.append(data)
    return ok(out)


@student_drives_bp.get("/organizations/<int:company_id>")
@role_required(Role.STUDENT)
def organization_detail(company_id):
    student = current_student()
    company = CompanyProfile.query.filter_by(
        id=company_id, approval_status=ApprovalStatus.APPROVED
    ).first()
    if company is None:
        raise NotFoundError("Company not found")
    data = company.to_dict()
    applied_ids = {a.drive_id for a in student.applications}
    drives = []
    for drive in company.drives:
        if drive.status != DriveStatus.APPROVED:
            continue
        item = to_student_dict(student, drive)
        item["applied"] = drive.id in applied_ids
        drives.append(item)
    data["drives"] = drives
    return ok(data)

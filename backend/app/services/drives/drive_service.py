"""Placement-drive lifecycle: company CRUD + admin approval/close."""
from app.extensions import db
from app.models.constants import DriveStatus
from app.models.placement.drive import PlacementDrive
from app.utils.errors import ApiError, ForbiddenError, NotFoundError

_EDITABLE = (
    "drive_name", "job_title", "job_description", "location", "package_lpa",
    "benefits", "skills_required", "min_experience", "eligible_branches",
    "min_cgpa", "eligible_years", "deadline",
)


def get_drive(drive_id: int) -> PlacementDrive:
    drive = db.session.get(PlacementDrive, drive_id)
    if drive is None:
        raise NotFoundError("Drive not found")
    return drive


def get_owned_drive(company, drive_id: int) -> PlacementDrive:
    drive = get_drive(drive_id)
    if drive.company_id != company.id:
        raise ForbiddenError("This drive belongs to another company")
    return drive


def list_company_drives(company_id: int):
    return (
        PlacementDrive.query.filter_by(company_id=company_id)
        .order_by(PlacementDrive.created_at.desc())
        .all()
    )


def _apply(drive: PlacementDrive, data: dict) -> None:
    for field in _EDITABLE:
        if field in data:
            setattr(drive, field, data[field])


def create_drive(company, data: dict) -> PlacementDrive:
    drive = PlacementDrive(company_id=company.id, status=DriveStatus.PENDING)
    _apply(drive, data)
    db.session.add(drive)
    db.session.commit()
    return drive


def update_drive(company, drive_id: int, data: dict) -> PlacementDrive:
    drive = get_owned_drive(company, drive_id)
    _apply(drive, data)
    db.session.commit()
    return drive


def company_set_status(company, drive_id: int, status: str) -> PlacementDrive:
    """Company opens (active) or closes an already-approved drive."""
    if status not in DriveStatus.COMPANY_SETTABLE:
        raise ApiError("Companies can only open or close a drive")
    drive = get_owned_drive(company, drive_id)
    if drive.status not in (DriveStatus.APPROVED, DriveStatus.CLOSED):
        raise ForbiddenError("Drive must be admin-approved first")
    drive.status = status
    db.session.commit()
    return drive


def set_drive_status(drive_id: int, status: str) -> PlacementDrive:
    if status not in DriveStatus.ALL:
        raise ApiError("Invalid drive status")
    drive = get_drive(drive_id)
    drive.status = status
    db.session.commit()
    return drive


def close_drive(drive_id: int) -> PlacementDrive:
    return set_drive_status(drive_id, DriveStatus.CLOSED)


def delete_drive(drive_id: int) -> None:
    db.session.delete(get_drive(drive_id))
    db.session.commit()

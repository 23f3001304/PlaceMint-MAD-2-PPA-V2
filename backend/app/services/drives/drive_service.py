"""Placement-drive lifecycle shared by admin (approve/close) and company."""
from app.extensions import db
from app.models.constants import DriveStatus
from app.models.placement.drive import PlacementDrive
from app.utils.errors import ApiError, NotFoundError


def get_drive(drive_id: int) -> PlacementDrive:
    drive = db.session.get(PlacementDrive, drive_id)
    if drive is None:
        raise NotFoundError("Drive not found")
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

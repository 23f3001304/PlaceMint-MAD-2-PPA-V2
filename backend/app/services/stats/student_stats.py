"""Student dashboard aggregates."""
from collections import Counter

from app.models.constants import ApplicationStatus, DriveStatus
from app.models.placement.drive import PlacementDrive

_IN_PROGRESS = {
    ApplicationStatus.SHORTLISTED,
    ApplicationStatus.INTERVIEW,
    ApplicationStatus.OFFER,
}


def student_dashboard(student) -> dict:
    apps = student.applications
    return {
        "applications": len(apps),
        "in_progress": sum(1 for a in apps if a.status in _IN_PROGRESS),
        "placements": len(student.placements),
        "open_drives": PlacementDrive.query.filter_by(status=DriveStatus.APPROVED).count(),
        "applications_by_status": dict(Counter(a.status for a in apps)),
    }

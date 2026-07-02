"""Company dashboard aggregates: drives, applications, shortlist, placements."""
from app.models.constants import ApplicationStatus, DriveStatus
from app.models.placement.application import Application
from app.models.placement.placement import Placement

_SHORTLISTED = (
    ApplicationStatus.SHORTLISTED,
    ApplicationStatus.INTERVIEW,
    ApplicationStatus.OFFER,
)


def company_dashboard(company) -> dict:
    drives = company.drives
    drive_ids = [d.id for d in drives]
    apps = Application.query.filter(Application.drive_id.in_(drive_ids))
    return {
        "drives": len(drives),
        "active_drives": sum(1 for d in drives if d.status == DriveStatus.APPROVED),
        "pending_drives": sum(1 for d in drives if d.status == DriveStatus.PENDING),
        "applications": apps.count() if drive_ids else 0,
        "shortlisted": apps.filter(Application.status.in_(_SHORTLISTED)).count()
        if drive_ids
        else 0,
        "placed": Placement.query.filter_by(company_id=company.id).count(),
    }

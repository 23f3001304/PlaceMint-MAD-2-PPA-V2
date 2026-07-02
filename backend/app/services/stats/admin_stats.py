"""Institute-wide aggregates for the admin dashboard and charts."""
from app.extensions import db
from app.models.constants import ApprovalStatus, DriveStatus
from app.models.placement.application import Application
from app.models.placement.drive import PlacementDrive
from app.models.placement.placement import Placement
from app.models.profiles.company import CompanyProfile
from app.models.profiles.student import StudentProfile


def dashboard_counts() -> dict:
    return {
        "students": StudentProfile.query.count(),
        "companies": CompanyProfile.query.count(),
        "pending_companies": CompanyProfile.query.filter_by(
            approval_status=ApprovalStatus.PENDING
        ).count(),
        "drives": PlacementDrive.query.count(),
        "pending_drives": PlacementDrive.query.filter_by(
            status=DriveStatus.PENDING
        ).count(),
        "applications": Application.query.count(),
        "placements": Placement.query.count(),
    }


def _count_by(column) -> dict:
    rows = db.session.query(column, db.func.count()).group_by(column).all()
    return {key: count for key, count in rows if key is not None}


def chart_data() -> dict:
    """Grouped counts shaped for Chart.js on the admin analytics view."""
    return {
        "applications_by_status": _count_by(Application.status),
        "drives_by_status": _count_by(PlacementDrive.status),
        "students_by_branch": _count_by(StudentProfile.branch),
    }

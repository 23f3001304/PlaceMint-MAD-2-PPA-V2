"""Company-side application review: status, feedback, interviews, placement.

The student-side `apply()` lives here too (added with the student milestone).
"""
from datetime import date, datetime

from app.extensions import db
from app.models.constants import ApplicationStatus, DriveStatus
from app.models.placement.application import Application
from app.models.placement.drive import PlacementDrive
from app.models.placement.placement import Placement
from app.services.drives.eligibility import eligibility_reasons
from app.utils.errors import ApiError, ConflictError, ForbiddenError, NotFoundError


def get_application(app_id: int) -> Application:
    app = db.session.get(Application, app_id)
    if app is None:
        raise NotFoundError("Application not found")
    return app


def apply(student, drive_id: int) -> Application:
    """Register a student's application, enforcing the Milestone-6 rules:
    approved-and-open drive, before the deadline, eligible, and not a duplicate.
    """
    drive = db.session.get(PlacementDrive, drive_id)
    if drive is None:
        raise NotFoundError("Drive not found")
    if drive.status != DriveStatus.APPROVED:
        raise ForbiddenError("This drive is not open for applications")
    if drive.deadline and drive.deadline < date.today():
        raise ForbiddenError("The application deadline has passed")
    if Application.query.filter_by(student_id=student.id, drive_id=drive.id).first():
        raise ConflictError("You have already applied to this drive")
    reasons = eligibility_reasons(student, drive)
    if reasons:
        raise ForbiddenError("Not eligible: " + ", ".join(reasons))

    application = Application(
        student_id=student.id, drive_id=drive.id, status=ApplicationStatus.APPLIED
    )
    db.session.add(application)
    db.session.commit()
    return application


def list_applicants(drive) -> list:
    return [a.to_dict(include_student=True) for a in drive.applications]


def _parse_dt(value):
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        raise ApiError("Invalid interview datetime")


def update_application(company, app_id: int, data: dict) -> Application:
    app = get_application(app_id)
    if app.drive.company_id != company.id:
        raise ForbiddenError("This application belongs to another company")

    status = data.get("status")
    if status is not None:
        if status not in ApplicationStatus.COMPANY_SETTABLE:
            raise ApiError("Invalid application status")
        app.status = status
    if "remarks" in data:
        app.remarks = (data.get("remarks") or "").strip() or None
    if data.get("interview_at"):
        app.interview_at = _parse_dt(data["interview_at"])
        app.interview_mode = (data.get("interview_mode") or "").strip() or None

    if app.status == ApplicationStatus.PLACED:
        _ensure_placement(app)
    db.session.commit()
    return app


def _ensure_placement(app: Application) -> None:
    if Placement.query.filter_by(application_id=app.id).first():
        return
    db.session.add(
        Placement(
            student_id=app.student_id, company_id=app.drive.company_id,
            drive_id=app.drive_id, application_id=app.id,
            position=app.drive.job_title, salary_lpa=app.drive.package_lpa or 0,
        )
    )

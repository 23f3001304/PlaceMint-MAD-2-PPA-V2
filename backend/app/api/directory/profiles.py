"""Read-only profile views behind the shareable, resume-grade profile pages.

Any signed-in user can view a company; admins and companies can view a student,
with the student's live application/placement activity attached for admins.
"""
from app.api.directory import directory_bp
from app.auth.rbac import current_user, role_required
from app.extensions import db
from app.models.constants import DriveStatus, Role
from app.models.profiles.company import CompanyProfile
from app.models.profiles.student import StudentProfile
from app.utils.errors import NotFoundError
from app.utils.responses import ok


@directory_bp.get("/students/<int:student_id>")
@role_required(Role.ADMIN, Role.COMPANY)
def student_profile(student_id):
    student = db.session.get(StudentProfile, student_id)
    if student is None:
        raise NotFoundError("Student not found")
    activity = _activity(student) if current_user().role == Role.ADMIN else None
    return ok({"profile": student.to_dict(), "activity": activity})


@directory_bp.get("/companies/<int:company_id>")
@role_required(Role.ADMIN, Role.COMPANY, Role.STUDENT)
def company_profile(company_id):
    company = db.session.get(CompanyProfile, company_id)
    if company is None:
        raise NotFoundError("Company not found")
    drives = [d.to_dict() for d in company.drives if d.status == DriveStatus.APPROVED]
    return ok({"profile": company.to_dict(), "drives": drives})


def _activity(student) -> dict:
    return {
        "applications": [a.to_dict(include_drive=True) for a in student.applications],
        "placements": [p.to_dict() for p in student.placements],
    }

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
    applicants = _company_applicants(company) if current_user().role == Role.ADMIN else None
    return ok({"profile": company.to_dict(), "drives": drives, "applicants": applicants})


def _activity(student) -> dict:
    return {
        "applications": [a.to_dict(include_drive=True) for a in student.applications],
        "placements": [p.to_dict() for p in student.placements],
    }


def _company_applicants(company) -> list:
    """Every student who applied to any of this company's drives (admin view)."""
    rows = []
    for drive in company.drives:
        for a in drive.applications:
            s = a.student
            rows.append({
                "id": a.id,
                "student_id": s.id if s else None,
                "student_name": s.name if s else None,
                "roll_no": s.roll_no if s else None,
                "drive": drive.job_title,
                "status": a.status,
                "applied_at": a.applied_at.isoformat() if a.applied_at else None,
            })
    return rows

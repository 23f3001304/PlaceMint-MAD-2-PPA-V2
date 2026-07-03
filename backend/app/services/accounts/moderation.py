"""Admin moderation: company approval, user blacklist/deactivate, deletion.

Deleting a company or student removes the underlying User; the model cascades
take care of the profile, its drives, applications and placements.
"""
from app.caching.keys import invalidate_admin, invalidate_company
from app.extensions import db
from app.models.constants import ApprovalStatus, Role
from app.models.profiles.company import CompanyProfile
from app.models.profiles.student import StudentProfile
from app.models.user import User
from app.utils.errors import ApiError, NotFoundError


def get_company(company_id: int) -> CompanyProfile:
    company = db.session.get(CompanyProfile, company_id)
    if company is None:
        raise NotFoundError("Company not found")
    return company


def get_student(student_id: int) -> StudentProfile:
    student = db.session.get(StudentProfile, student_id)
    if student is None:
        raise NotFoundError("Student not found")
    return student


def _moderatable_user(user_id: int) -> User:
    user = db.session.get(User, user_id)
    if user is None:
        raise NotFoundError("User not found")
    if user.role == Role.ADMIN:
        raise ApiError("Cannot moderate an admin account", status=403)
    return user


def set_company_approval(company_id: int, status: str) -> CompanyProfile:
    if status not in ApprovalStatus.ALL:
        raise ApiError("Invalid approval status")
    company = get_company(company_id)
    company.approval_status = status
    db.session.commit()
    invalidate_company(company.id)
    return company


def set_user_active(user_id: int, active: bool) -> User:
    user = _moderatable_user(user_id)
    user.is_active = bool(active)
    db.session.commit()
    invalidate_admin()
    return user


def set_user_blacklist(user_id: int, blacklisted: bool) -> User:
    user = _moderatable_user(user_id)
    user.is_blacklisted = bool(blacklisted)
    db.session.commit()
    invalidate_admin()
    return user


def delete_company(company_id: int) -> None:
    db.session.delete(get_company(company_id).user)
    db.session.commit()
    invalidate_admin()


def delete_student(student_id: int) -> None:
    db.session.delete(get_student(student_id).user)
    db.session.commit()
    invalidate_admin()

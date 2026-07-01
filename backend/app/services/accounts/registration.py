"""Create student and company accounts (unified User + role profile)."""
from app.auth.passwords import hash_password
from app.extensions import db
from app.models.constants import Role
from app.models.profiles.company import CompanyProfile
from app.models.profiles.student import StudentProfile
from app.models.user import User
from app.utils.errors import ConflictError


def _ensure_email_free(email: str) -> None:
    if User.query.filter_by(email=email).first():
        raise ConflictError("Email already registered")


def register_student(data: dict) -> User:
    _ensure_email_free(data["email"])
    if StudentProfile.query.filter_by(roll_no=data["roll_no"]).first():
        raise ConflictError("Roll number already registered")

    user = User(
        email=data["email"],
        password_hash=hash_password(data["password"]),
        role=Role.STUDENT,
    )
    user.student_profile = StudentProfile(
        name=data["name"],
        roll_no=data["roll_no"],
        branch=data["branch"],
        degree=data.get("degree"),
        cgpa=data["cgpa"],
        grad_year=data["grad_year"],
        phone=data.get("phone"),
        skills=data.get("skills") or [],
        experience=data.get("experience"),
    )
    db.session.add(user)
    db.session.commit()
    return user


def register_company(data: dict) -> User:
    _ensure_email_free(data["email"])

    user = User(
        email=data["email"],
        password_hash=hash_password(data["password"]),
        role=Role.COMPANY,
    )
    user.company_profile = CompanyProfile(
        company_name=data["company_name"],
        industry=data.get("industry"),
        location=data.get("location"),
        hr_contact=data.get("hr_contact"),
        website=data.get("website"),
        description=data.get("description"),
    )
    db.session.add(user)
    db.session.commit()
    return user

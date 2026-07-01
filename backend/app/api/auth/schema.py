"""Normalize and validate auth request bodies before they hit the services."""
from app.models.constants import Role
from app.utils.errors import ApiError
from app.utils.validation import as_float, as_int, as_list, require, valid_email

MIN_PASSWORD_LEN = 6


def clean_login(data: dict) -> dict:
    require(data, "email", "password")
    return {"email": data["email"].strip().lower(), "password": data["password"]}


def clean_registration(data: dict) -> tuple[str, dict]:
    role = data.get("role")
    if role not in Role.REGISTERABLE:
        raise ApiError("Role must be 'student' or 'company'")
    require(data, "email", "password")
    valid_email(data["email"])
    if len(data["password"]) < MIN_PASSWORD_LEN:
        raise ApiError(f"Password must be at least {MIN_PASSWORD_LEN} characters")

    base = {"email": data["email"].strip().lower(), "password": data["password"]}
    fields = _student_fields(data) if role == Role.STUDENT else _company_fields(data)
    return role, {**base, **fields}


def _student_fields(data: dict) -> dict:
    require(data, "name", "roll_no", "branch", "grad_year")
    return {
        "name": data["name"].strip(),
        "roll_no": data["roll_no"].strip(),
        "branch": data["branch"].strip(),
        "degree": _clean(data.get("degree")),
        "cgpa": as_float(data.get("cgpa"), "CGPA"),
        "grad_year": as_int(data.get("grad_year"), "graduation year"),
        "phone": _clean(data.get("phone")),
        "skills": as_list(data.get("skills")),
        "experience": _clean(data.get("experience")),
    }


def _company_fields(data: dict) -> dict:
    require(data, "company_name")
    return {
        "company_name": data["company_name"].strip(),
        "industry": _clean(data.get("industry")),
        "location": _clean(data.get("location")),
        "hr_contact": _clean(data.get("hr_contact")),
        "website": _clean(data.get("website")),
        "description": _clean(data.get("description")),
    }


def _clean(value):
    cleaned = (value or "").strip()
    return cleaned or None

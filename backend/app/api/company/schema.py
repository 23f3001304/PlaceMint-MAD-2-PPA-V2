"""Validate/normalize company drive and profile payloads."""
from datetime import date

from app.utils.errors import ApiError
from app.utils.validation import as_float, as_list, require

_PROFILE_FIELDS = ("company_name", "industry", "location", "hr_contact", "website", "description")


def _clean(value):
    cleaned = (value or "").strip()
    return cleaned or None


def _parse_date(value):
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError):
        raise ApiError("Invalid deadline (use YYYY-MM-DD)")


def _years(value):
    out = []
    for year in as_list(value):
        try:
            out.append(int(year))
        except (TypeError, ValueError):
            raise ApiError("Eligible years must be numbers")
    return out


def clean_drive(data: dict) -> dict:
    require(data, "job_title", "job_description", "deadline")
    return {
        "drive_name": _clean(data.get("drive_name")),
        "job_title": data["job_title"].strip(),
        "job_description": data["job_description"].strip(),
        "location": _clean(data.get("location")),
        "package_lpa": as_float(data.get("package_lpa"), "package"),
        "benefits": _clean(data.get("benefits")),
        "skills_required": as_list(data.get("skills_required")),
        "min_experience": as_float(data.get("min_experience"), "experience"),
        "eligible_branches": as_list(data.get("eligible_branches")),
        "min_cgpa": as_float(data.get("min_cgpa"), "CGPA"),
        "eligible_years": _years(data.get("eligible_years")),
        "deadline": _parse_date(data["deadline"]),
    }


def clean_company_profile(data: dict) -> dict:
    out = {field: _clean(data[field]) for field in _PROFILE_FIELDS if field in data}
    if "company_name" in out and not out["company_name"]:
        raise ApiError("Company name cannot be empty")
    return out

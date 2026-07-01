"""Small boundary validators.

Every API handler runs untrusted input through these before it reaches a
service, so services can trust the shapes they receive (dev-principles: validate
at the edge, trust internally).
"""
import re

from app.utils.errors import ApiError

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def require(data: dict, *fields: str) -> None:
    missing = [f for f in fields if data.get(f) in (None, "", [])]
    if missing:
        raise ApiError("Missing required fields: " + ", ".join(missing))


def valid_email(email: str) -> None:
    if not EMAIL_RE.match((email or "").strip()):
        raise ApiError("Invalid email address")


def as_float(value, field: str, default: float = 0.0) -> float:
    if value in (None, ""):
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        raise ApiError(f"{field} must be a number")


def as_int(value, field: str, default=None) -> int:
    if value in (None, "") and default is not None:
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        raise ApiError(f"{field} must be an integer")


def as_list(value) -> list:
    """Accept a JSON array or a comma-separated string; return a clean list."""
    if value in (None, ""):
        return []
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    return [part.strip() for part in str(value).split(",") if part.strip()]

"""Role-based access control.

`role_required` guards a route: it verifies the JWT, loads the user, refuses
deactivated/blacklisted accounts, and checks the role claim. The loaded user is
cached on `flask.g` so handlers can call `current_user()` without a second query.
"""
from functools import wraps

from flask import g
from flask_jwt_extended import get_jwt, get_jwt_identity, verify_jwt_in_request

from app.extensions import db
from app.models.user import User
from app.utils.errors import ApiError, ForbiddenError


def current_user() -> User | None:
    if "current_user" not in g:
        identity = get_jwt_identity()
        g.current_user = db.session.get(User, int(identity)) if identity is not None else None
    return g.current_user


def _ensure_active(user: User | None) -> None:
    if user is None:
        raise ApiError("Account not found", status=401)
    if not user.can_login:
        raise ForbiddenError("Account is deactivated or blacklisted")


def role_required(*roles: str):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            user = current_user()
            _ensure_active(user)
            if roles and get_jwt().get("role") not in roles:
                raise ForbiddenError("Insufficient permissions for this action")
            return fn(*args, **kwargs)

        return wrapper

    return decorator


def current_company():
    """The signed-in user's company profile (assumes a company-guarded route)."""
    user = current_user()
    if user is None or user.company_profile is None:
        raise ForbiddenError("Company profile required")
    return user.company_profile


def current_student():
    user = current_user()
    if user is None or user.student_profile is None:
        raise ForbiddenError("Student profile required")
    return user.student_profile


def approved_company():
    """Guard company actions (posting/managing drives) behind admin approval."""
    company = current_company()
    if not company.is_approved:
        raise ForbiddenError("Your company is awaiting admin approval")
    return company

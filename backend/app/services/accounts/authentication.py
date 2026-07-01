"""Verify credentials and mint JWTs carrying the user's role claim."""
from flask_jwt_extended import create_access_token

from app.auth.passwords import verify_password
from app.models.user import User
from app.utils.errors import ApiError, ForbiddenError


def authenticate(email: str, password: str) -> User:
    user = User.query.filter_by(email=email).first()
    if user is None or not verify_password(user.password_hash, password):
        raise ApiError("Invalid email or password", status=401)
    if not user.can_login:
        raise ForbiddenError("Account is deactivated or blacklisted")
    return user


def profile_of(user: User) -> dict | None:
    if user.student_profile:
        return user.student_profile.to_dict()
    if user.company_profile:
        return user.company_profile.to_dict()
    return None


def build_auth_payload(user: User) -> dict:
    """Token + user + profile: everything the SPA needs to bootstrap a session."""
    token = create_access_token(
        identity=user.id, additional_claims={"role": user.role}
    )
    return {"token": token, "user": user.to_dict(), "profile": profile_of(user)}

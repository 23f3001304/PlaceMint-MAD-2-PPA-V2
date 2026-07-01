"""Authentication endpoints: register, login, and the current-session lookup."""
from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.api.auth.schema import clean_login, clean_registration
from app.auth.rbac import current_user
from app.models.constants import Role
from app.services.accounts.authentication import (
    authenticate,
    build_auth_payload,
    profile_of,
)
from app.services.accounts.registration import register_company, register_student
from app.utils.responses import created, ok

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/register")
def register():
    role, data = clean_registration(request.get_json(silent=True) or {})
    user = register_student(data) if role == Role.STUDENT else register_company(data)
    return created(build_auth_payload(user))


@auth_bp.post("/login")
def login():
    data = clean_login(request.get_json(silent=True) or {})
    user = authenticate(data["email"], data["password"])
    return ok(build_auth_payload(user))


@auth_bp.get("/me")
@jwt_required()
def me():
    user = current_user()
    return ok({"user": user.to_dict(), "profile": profile_of(user)})

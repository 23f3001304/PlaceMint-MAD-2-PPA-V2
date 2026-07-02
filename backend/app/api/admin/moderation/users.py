"""Generic account moderation (blacklist / deactivate) by user id.

Works for both company and student accounts since both are Users; the SPA
passes the row's user_id.
"""
from flask import Blueprint, request

from app.auth.rbac import role_required
from app.models.constants import Role
from app.services.accounts.moderation import set_user_active, set_user_blacklist
from app.utils.responses import ok

admin_users_bp = Blueprint("admin_users", __name__)


@admin_users_bp.post("/<int:user_id>/blacklist")
@role_required(Role.ADMIN)
def blacklist(user_id):
    value = bool((request.get_json(silent=True) or {}).get("blacklisted", True))
    return ok(set_user_blacklist(user_id, value).to_dict())


@admin_users_bp.post("/<int:user_id>/active")
@role_required(Role.ADMIN)
def active(user_id):
    value = bool((request.get_json(silent=True) or {}).get("active", True))
    return ok(set_user_active(user_id, value).to_dict())

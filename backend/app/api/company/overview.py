"""Company dashboard stats and own-profile view/edit."""
import os

from flask import Blueprint, current_app, request
from werkzeug.utils import secure_filename

from app.api.company.schema import clean_company_profile
from app.auth.rbac import current_company, role_required
from app.caching.keys import STATS_TTL, company_stats_key, get_or_set
from app.extensions import db
from app.models.constants import Role
from app.services.stats.company_stats import company_dashboard
from app.utils.errors import ApiError
from app.utils.responses import ok

company_overview_bp = Blueprint("company_overview", __name__)

_ALLOWED_LOGO = {".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif"}


@company_overview_bp.get("/stats")
@role_required(Role.COMPANY)
def stats():
    company = current_company()
    return ok(get_or_set(company_stats_key(company.id), STATS_TTL, lambda: company_dashboard(company)))


@company_overview_bp.get("/profile")
@role_required(Role.COMPANY)
def get_profile():
    return ok(current_company().to_dict())


@company_overview_bp.patch("/profile")
@role_required(Role.COMPANY)
def update_profile():
    company = current_company()
    for key, value in clean_company_profile(request.get_json(silent=True) or {}).items():
        setattr(company, key, value)
    db.session.commit()
    return ok(company.to_dict())


@company_overview_bp.post("/logo")
@role_required(Role.COMPANY)
def upload_logo():
    company = current_company()
    file = request.files.get("logo")
    if file is None or not file.filename:
        raise ApiError("No file provided")
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in _ALLOWED_LOGO:
        raise ApiError("Logo must be an image (PNG, JPG, WEBP or SVG)")
    filename = secure_filename(f"logo_{company.id}{ext}")
    file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
    company.logo_path = filename
    db.session.commit()
    return ok(company.to_dict())

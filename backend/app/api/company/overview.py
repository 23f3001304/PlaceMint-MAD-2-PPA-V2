"""Company dashboard stats and own-profile view/edit."""
from flask import Blueprint, request

from app.api.company.schema import clean_company_profile
from app.auth.rbac import current_company, role_required
from app.extensions import db
from app.models.constants import Role
from app.services.stats.company_stats import company_dashboard
from app.utils.responses import ok

company_overview_bp = Blueprint("company_overview", __name__)


@company_overview_bp.get("/stats")
@role_required(Role.COMPANY)
def stats():
    return ok(company_dashboard(current_company()))


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

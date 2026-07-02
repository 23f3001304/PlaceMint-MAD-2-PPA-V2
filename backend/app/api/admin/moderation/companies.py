"""Admin company management: search/list, approve or reject, remove."""
from flask import Blueprint, request

from app.auth.rbac import role_required
from app.models.constants import ApprovalStatus, Role
from app.models.profiles.company import CompanyProfile
from app.services.accounts.moderation import delete_company, set_company_approval
from app.utils.responses import ok, serve_page

admin_companies_bp = Blueprint("admin_companies", __name__)


@admin_companies_bp.get("")
@role_required(Role.ADMIN)
def list_companies():
    query = CompanyProfile.query
    status = request.args.get("status")
    if status in ApprovalStatus.ALL:
        query = query.filter_by(approval_status=status)
    q = request.args.get("q", "").strip()
    if q:
        like = f"%{q}%"
        query = query.filter(
            CompanyProfile.company_name.ilike(like) | CompanyProfile.industry.ilike(like)
        )
    return serve_page(query.order_by(CompanyProfile.created_at.desc()), lambda c: c.to_dict())


@admin_companies_bp.post("/<int:company_id>/approval")
@role_required(Role.ADMIN)
def approval(company_id):
    status = (request.get_json(silent=True) or {}).get("status")
    return ok(set_company_approval(company_id, status).to_dict())


@admin_companies_bp.delete("/<int:company_id>")
@role_required(Role.ADMIN)
def remove(company_id):
    delete_company(company_id)
    return ok({"deleted": company_id})

"""Role-aware document serving: student resumes and generated offer letters."""
import os

from flask import Blueprint, Response, current_app, send_file
from flask_jwt_extended import jwt_required

from app.auth.rbac import current_user
from app.extensions import db
from app.models.constants import Role
from app.models.placement.placement import Placement
from app.models.profiles.student import StudentProfile
from app.utils.errors import ForbiddenError, NotFoundError

documents_bp = Blueprint("documents", __name__)


def _can_view_resume(user, student) -> bool:
    if user.role == Role.ADMIN:
        return True
    if user.role == Role.STUDENT:
        return user.student_profile and user.student_profile.id == student.id
    if user.role == Role.COMPANY and user.company_profile:
        company_id = user.company_profile.id
        return any(a.drive.company_id == company_id for a in student.applications)
    return False


@documents_bp.get("/resume/<int:student_id>")
@jwt_required()
def resume(student_id):
    student = db.session.get(StudentProfile, student_id)
    if student is None or not student.resume_path:
        raise NotFoundError("No resume on file")
    if not _can_view_resume(current_user(), student):
        raise ForbiddenError("Not allowed to view this resume")
    path = os.path.join(current_app.config["UPLOAD_FOLDER"], student.resume_path)
    if not os.path.exists(path):
        raise NotFoundError("Resume file is missing")
    return send_file(path, download_name=student.resume_path)


@documents_bp.get("/offer-letter/<int:placement_id>")
@jwt_required()
def offer_letter(placement_id):
    placement = db.session.get(Placement, placement_id)
    if placement is None:
        raise NotFoundError("Placement not found")
    user = current_user()
    allowed = (
        user.role == Role.ADMIN
        or (user.role == Role.STUDENT and user.student_profile and user.student_profile.id == placement.student_id)
        or (user.role == Role.COMPANY and user.company_profile and user.company_profile.id == placement.company_id)
    )
    if not allowed:
        raise ForbiddenError("Not allowed to view this offer letter")
    return Response(_render_offer_letter(placement), mimetype="text/html")


def _render_offer_letter(p: Placement) -> str:
    company = p.company.company_name if p.company else "The Company"
    student = p.student.name if p.student else "Candidate"
    joining = p.joining_date.strftime("%d %B %Y") if p.joining_date else "to be confirmed"
    return (
        '<!doctype html><html><head><meta charset="utf-8"><title>Offer Letter</title></head>'
        '<body style="font-family:Georgia,\'Times New Roman\',serif;max-width:720px;margin:48px auto;'
        'color:#14110f;padding:0 28px;line-height:1.7">'
        f'<div style="font-size:26px;font-weight:700;color:#1f6b3a">{company}</div>'
        '<hr style="border:none;border-top:2px solid #1f6b3a;margin:12px 0 28px">'
        '<p style="text-align:right;color:#6b6357">Offer of Employment</p>'
        f'<p>Dear {student},</p>'
        f'<p>We are delighted to offer you the position of <strong>{p.position}</strong> at '
        f'{company}. Based on your performance through our placement process, we believe you '
        'will be a strong addition to our team.</p>'
        '<p>The key terms of your offer are:</p>'
        '<ul>'
        f'<li>Position: <strong>{p.position}</strong></li>'
        f'<li>Annual compensation: <strong>{p.salary_lpa} LPA</strong></li>'
        f'<li>Proposed joining date: <strong>{joining}</strong></li>'
        '</ul>'
        '<p>We look forward to welcoming you aboard.</p>'
        '<p style="margin-top:36px">Warm regards,<br>Talent Acquisition<br>'
        f'<strong>{company}</strong></p>'
        '</body></html>'
    )

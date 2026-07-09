"""Student profile: view/edit, dashboard stats, and resume upload."""
import os

from flask import Blueprint, current_app, request
from werkzeug.utils import secure_filename

from app.auth.rbac import current_student, role_required
from app.caching.keys import STATS_TTL, get_or_set, student_stats_key
from app.extensions import db
from app.models.constants import Role
from app.services.stats.student_stats import student_dashboard
from app.utils.errors import ApiError
from app.utils.responses import ok
from app.utils.validation import as_float, as_int, as_list, clean_links

student_profile_bp = Blueprint("student_profile", __name__)

_ALLOWED_RESUME = {".pdf", ".doc", ".docx"}
_EDITABLE_STR = ("name", "branch", "degree", "phone", "experience")


@student_profile_bp.get("")
@role_required(Role.STUDENT)
def get_profile():
    return ok(current_student().to_dict())


@student_profile_bp.get("/stats")
@role_required(Role.STUDENT)
def stats():
    student = current_student()
    return ok(get_or_set(student_stats_key(student.id), STATS_TTL, lambda: student_dashboard(student)))


@student_profile_bp.patch("")
@role_required(Role.STUDENT)
def update_profile():
    student = current_student()
    data = request.get_json(silent=True) or {}
    for field in _EDITABLE_STR:
        if field in data:
            setattr(student, field, (data[field] or "").strip() or None)
    if "cgpa" in data:
        student.cgpa = as_float(data.get("cgpa"), "CGPA")
    if "grad_year" in data:
        student.grad_year = as_int(data.get("grad_year"), "graduation year", student.grad_year)
    if "skills" in data:
        student.skills = as_list(data.get("skills"))
    if "links" in data:
        student.links = clean_links(data.get("links"), 3)
    if data.get("onboarded"):
        student.onboarded = True
    if not student.name:
        raise ApiError("Name cannot be empty")
    db.session.commit()
    return ok(student.to_dict())


@student_profile_bp.post("/resume")
@role_required(Role.STUDENT)
def upload_resume():
    student = current_student()
    file = request.files.get("resume")
    if file is None or not file.filename:
        raise ApiError("No file provided")
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in _ALLOWED_RESUME:
        raise ApiError("Resume must be a PDF or Word document")
    filename = secure_filename(f"resume_{student.id}{ext}")
    file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
    student.resume_path = filename
    db.session.commit()
    return ok(student.to_dict())

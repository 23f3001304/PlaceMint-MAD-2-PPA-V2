"""Admin student management: search/list, detail with history, remove."""
from flask import Blueprint, request

from app.auth.rbac import role_required
from app.models.constants import Role
from app.models.profiles.student import StudentProfile
from app.services.accounts.moderation import delete_student, get_student
from app.utils.responses import ok, serve_page

admin_students_bp = Blueprint("admin_students", __name__)


@admin_students_bp.get("")
@role_required(Role.ADMIN)
def list_students():
    query = StudentProfile.query
    q = request.args.get("q", "").strip()
    if q:
        like = f"%{q}%"
        query = query.filter(
            StudentProfile.name.ilike(like) | StudentProfile.roll_no.ilike(like)
        )
    return serve_page(query.order_by(StudentProfile.name), lambda s: s.to_dict())


@admin_students_bp.get("/<int:student_id>")
@role_required(Role.ADMIN)
def detail(student_id):
    student = get_student(student_id)
    data = student.to_dict()
    data["applications"] = [a.to_dict(include_drive=True) for a in student.applications]
    return ok(data)


@admin_students_bp.delete("/<int:student_id>")
@role_required(Role.ADMIN)
def remove(student_id):
    delete_student(student_id)
    return ok({"deleted": student_id})

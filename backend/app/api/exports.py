"""User-triggered CSV export: start a job, poll status, download the result.

Shared by students and companies; the export contents depend on the caller's
role. Ownership is checked on both status and download.
"""
import os

from flask import Blueprint, current_app, send_file
from flask_jwt_extended import jwt_required

from app.auth.rbac import current_user
from app.extensions import db
from app.models.constants import Role
from app.models.export_job import ExportJob
from app.tasks.exports import run_export
from app.utils.errors import ForbiddenError, NotFoundError
from app.utils.responses import created, ok

exports_bp = Blueprint("exports", __name__)


def _owned_job(job_id: int) -> ExportJob:
    job = db.session.get(ExportJob, job_id)
    if job is None or job.user_id != current_user().id:
        raise NotFoundError("Export not found")
    return job


@exports_bp.post("")
@jwt_required()
def start_export():
    user = current_user()
    if user.role not in (Role.STUDENT, Role.COMPANY):
        raise ForbiddenError("Only students and companies can export")
    job = ExportJob(user_id=user.id, role=user.role, status="pending")
    db.session.add(job)
    db.session.commit()
    run_export.delay(job.id)
    return created(job.to_dict())


@exports_bp.get("/<int:job_id>")
@jwt_required()
def export_status(job_id):
    return ok(_owned_job(job_id).to_dict())


@exports_bp.get("/<int:job_id>/download")
@jwt_required()
def export_download(job_id):
    job = _owned_job(job_id)
    if job.status != "done" or not job.filename:
        raise NotFoundError("Export is not ready yet")
    path = os.path.join(current_app.config["EXPORT_FOLDER"], job.filename)
    if not os.path.exists(path):
        raise NotFoundError("Export file is missing")
    return send_file(path, as_attachment=True, download_name=job.filename)

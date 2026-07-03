"""Build a user's application history CSV and mark the export job complete.

Kept as a plain function (not the task itself) so it runs and tests without a
broker; the Celery task is a thin wrapper around it.
"""
import csv
import os

from flask import current_app

from app.extensions import db
from app.models.constants import Role
from app.models.export_job import ExportJob
from app.models.user import User
from app.utils.email import send_email

_STUDENT_HEADERS = ["Student ID", "Company", "Drive Title", "Status", "Applied On", "Interview"]
_COMPANY_HEADERS = ["Student", "Student ID", "Drive Title", "Status", "Applied On"]


def _student_rows(user: User):
    for app in user.student_profile.applications:
        drive = app.drive
        yield [
            user.student_profile.roll_no,
            drive.company.company_name if drive and drive.company else "",
            drive.job_title if drive else "",
            app.status,
            app.applied_at.date().isoformat() if app.applied_at else "",
            app.interview_at.isoformat(sep=" ")[:16] if app.interview_at else "",
        ]


def _company_rows(user: User):
    for drive in user.company_profile.drives:
        for app in drive.applications:
            yield [
                app.student.name if app.student else "",
                app.student.roll_no if app.student else "",
                drive.job_title,
                app.status,
                app.applied_at.date().isoformat() if app.applied_at else "",
            ]


def build_export(job_id: int) -> dict:
    job = db.session.get(ExportJob, job_id)
    if job is None:
        return {"error": "job not found"}
    job.status = "running"
    db.session.commit()

    user = db.session.get(User, job.user_id)
    if user.role == Role.STUDENT:
        headers, rows = _STUDENT_HEADERS, list(_student_rows(user))
    else:
        headers, rows = _COMPANY_HEADERS, list(_company_rows(user))

    filename = f"export_{job.role}_{job.user_id}_{job.id}.csv"
    path = os.path.join(current_app.config["EXPORT_FOLDER"], filename)
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(headers)
        writer.writerows(rows)

    job.status = "done"
    job.filename = filename
    job.row_count = len(rows)
    db.session.commit()

    send_email(
        user.email, "Your application export is ready",
        f"<p>Your export of {len(rows)} rows is ready to download from your dashboard.</p>",
        text=f"Your export of {len(rows)} rows is ready.",
    )
    return {"file": filename, "rows": len(rows)}

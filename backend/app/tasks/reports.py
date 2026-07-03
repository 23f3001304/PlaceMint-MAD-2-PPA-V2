"""Monthly report job: an institute report to the admin and one per company."""
from datetime import date

from celery import shared_task
from flask import current_app

from app.models.constants import ApprovalStatus
from app.models.placement.application import Application
from app.models.placement.drive import PlacementDrive
from app.models.placement.placement import Placement
from app.models.profiles.company import CompanyProfile
from app.models.profiles.student import StudentProfile
from app.utils.email import send_email


def _table(rows) -> str:
    cells = "".join(
        f'<tr><td style="padding:6px 14px 6px 0;color:#6b6357">{label}</td>'
        f'<td style="padding:6px 0;font-weight:700">{value}</td></tr>'
        for label, value in rows
    )
    return f'<table style="border-collapse:collapse;margin-top:12px">{cells}</table>'


def _wrap(title: str, body: str) -> str:
    return (
        '<div style="font-family:Arial,Helvetica,sans-serif;max-width:640px;color:#14110f">'
        f'<h2 style="color:#1f6b3a;margin-bottom:4px">{title}</h2>'
        f'<p style="color:#6b6357">Generated {date.today():%d %B %Y}</p>{body}</div>'
    )


def _send_admin_report() -> None:
    body = _table([
        ("Students registered", StudentProfile.query.count()),
        ("Companies registered", CompanyProfile.query.count()),
        ("Drives conducted", PlacementDrive.query.count()),
        ("Applications received", Application.query.count()),
        ("Students placed", Placement.query.count()),
    ])
    html = _wrap(f"Placement report - {date.today():%B %Y}", body)
    send_email(current_app.config["ADMIN_EMAIL"], f"Monthly placement report - {date.today():%B %Y}",
               html, text="Monthly placement report")


def _send_company_reports() -> int:
    count = 0
    for company in CompanyProfile.query.filter_by(approval_status=ApprovalStatus.APPROVED).all():
        drive_ids = [d.id for d in company.drives]
        applications = Application.query.filter(Application.drive_id.in_(drive_ids)).count() if drive_ids else 0
        body = _table([
            ("Drives posted", len(company.drives)),
            ("Applications received", applications),
            ("Candidates placed", len(company.placements)),
        ])
        html = _wrap(f"{company.company_name} - hiring report", body)
        if company.user:
            send_email(company.user.email, f"Your monthly hiring report - {date.today():%B %Y}",
                       html, text="Monthly hiring report")
            count += 1
    return count


def run_monthly_reports() -> dict:
    _send_admin_report()
    return {"admin_report": 1, "company_reports": _send_company_reports()}


@shared_task(name="app.tasks.reports.send_monthly_reports")
def send_monthly_reports() -> dict:
    return run_monthly_reports()

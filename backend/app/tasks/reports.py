"""Monthly report job: an institute report to the admin and one per company."""
from datetime import date
from html import escape

from celery import shared_task
from flask import current_app

from app.models.constants import ApprovalStatus
from app.models.placement.application import Application
from app.models.placement.drive import PlacementDrive
from app.models.placement.placement import Placement
from app.models.profiles.company import CompanyProfile
from app.models.profiles.student import StudentProfile
from app.utils.email import send_email


# ── inline-style helpers (PlaceMint palette) ─────────────────────────────
def _stat_card(icon: str, label: str, value) -> str:
    return (
        f'<td style="padding:12px;text-align:center;vertical-align:top;">'
        f'<div style="font-size:24px;margin-bottom:4px;">{icon}</div>'
        f'<div style="font-size:28px;font-weight:700;color:#1f6b3a;">{value}</div>'
        f'<div style="font-size:12px;color:#6b6357;text-transform:uppercase;'
        f'letter-spacing:0.5px;margin-top:2px;">{label}</div>'
        f'</td>'
    )


def _stat_row(cards_html: str) -> str:
    return (
        f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" '
        f'width="100%" style="background-color:#faf8f5;border:1px solid '
        f'rgba(20,17,15,0.08);border-radius:8px;margin:16px 0;">'
        f'<tr>{cards_html}</tr></table>'
    )


def _send_admin_report() -> None:
    month_label = date.today().strftime("%B %Y")
    students = StudentProfile.query.count()
    companies = CompanyProfile.query.count()
    drives = PlacementDrive.query.count()
    applications = Application.query.count()
    placed = Placement.query.count()

    stats = (
        _stat_card("🎓", "Students", students)
        + _stat_card("🏢", "Companies", companies)
        + _stat_card("📋", "Drives", drives)
    )
    stats2 = (
        _stat_card("📝", "Applications", applications)
        + _stat_card("✅", "Placed", placed)
    )

    body = f"""
<p style="margin:0 0 8px 0;font-size:15px;color:#14110f;">
  Hi Admin,
</p>
<p style="margin:0 0 20px 0;font-size:15px;color:#14110f;">
  Here is the monthly placement summary for <strong style="color:#1f6b3a;">{month_label}</strong>.
</p>

{_stat_row(stats)}
{_stat_row(stats2)}

<p style="font-size:13px;color:#6b6357;margin-top:20px;">
  Generated on {date.today().strftime("%d %B %Y")}. Log in to the PlaceMint admin
  dashboard for detailed analytics.
</p>
"""
    send_email(
        current_app.config["ADMIN_EMAIL"],
        f"📊 Mint University Placement Report — {month_label}",
        body,
        text="Monthly placement report",
    )


def _send_company_reports() -> int:
    month_label = date.today().strftime("%B %Y")
    count = 0
    for company in CompanyProfile.query.filter_by(approval_status=ApprovalStatus.APPROVED).all():
        drive_ids = [d.id for d in company.drives]
        applications = Application.query.filter(Application.drive_id.in_(drive_ids)).count() if drive_ids else 0
        name = escape(company.company_name)

        stats = (
            _stat_card("📋", "Drives Posted", len(company.drives))
            + _stat_card("📝", "Applications", applications)
            + _stat_card("✅", "Placed", len(company.placements))
        )

        body = f"""
<p style="margin:0 0 8px 0;font-size:15px;color:#14110f;">
  Hello <strong style="color:#1f6b3a;">{name}</strong> team,
</p>
<p style="margin:0 0 20px 0;font-size:15px;color:#14110f;">
  Here is your hiring activity summary for <strong style="color:#1f6b3a;">{month_label}</strong>
  on PlaceMint.
</p>

{_stat_row(stats)}

<p style="font-size:13px;color:#6b6357;margin-top:20px;">
  Generated on {date.today().strftime("%d %B %Y")}. Visit your PlaceMint company
  dashboard for the full breakdown.
</p>
"""
        if company.user:
            send_email(
                company.user.email,
                f"📊 Your Monthly Hiring Report — {month_label}",
                body,
                text="Monthly hiring report",
            )
            count += 1
    return count


def run_monthly_reports() -> dict:
    _send_admin_report()
    return {"admin_report": 1, "company_reports": _send_company_reports()}


@shared_task(name="app.tasks.reports.send_monthly_reports")
def send_monthly_reports() -> dict:
    return run_monthly_reports()


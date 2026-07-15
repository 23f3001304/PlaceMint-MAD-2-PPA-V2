"""Daily reminder job: upcoming interviews and approaching drive deadlines."""
from datetime import date, timedelta

from celery import shared_task
from flask import current_app

from app.models.constants import DriveStatus
from app.models.placement.application import Application
from app.models.placement.drive import PlacementDrive
from app.models.profiles.student import StudentProfile
from app.services.drives.eligibility import eligibility_reasons
from app.utils.email import send_email


# ── inline-style constants (PlaceMint palette) ──────────────────────────
_CARD = (
    'style="background-color:#faf8f5;border:1px solid rgba(20,17,15,0.08);'
    'border-radius:8px;padding:20px 24px;margin:16px 0;"'
)
_LABEL = 'style="display:block;font-size:12px;color:#6b6357;margin-bottom:2px;text-transform:uppercase;letter-spacing:0.5px;"'
_VALUE = 'style="font-size:15px;color:#14110f;font-weight:600;"'
_ACCENT = 'style="color:#1f6b3a;font-weight:700;"'
_BADGE = (
    'style="display:inline-block;background-color:#1f6b3a;color:#efe9dc;'
    'font-size:12px;font-weight:600;padding:4px 12px;border-radius:20px;'
    'letter-spacing:0.3px;"'
)
_MUTED = 'style="font-size:13px;color:#6b6357;margin-top:16px;"'


def _detail_row(icon: str, label: str, value: str) -> str:
    return (
        f'<tr>'
        f'<td style="padding:6px 12px 6px 0;vertical-align:top;font-size:16px;width:28px;">{icon}</td>'
        f'<td style="padding:6px 0;">'
        f'<span {_LABEL}>{label}</span>'
        f'<span {_VALUE}>{value}</span>'
        f'</td>'
        f'</tr>'
    )


def _interview_reminders() -> int:
    today = date.today()
    horizon = today + timedelta(days=2)
    count = 0
    for app in Application.query.filter(Application.interview_at.isnot(None)).all():
        if today <= app.interview_at.date() <= horizon and app.student and app.student.user:
            name = app.student.name or "Student"
            title = app.drive.job_title
            company = app.drive.company.company_name
            dt = app.interview_at.strftime("%d %B %Y at %H:%M")
            mode = app.interview_mode or "TBD"

            body = f"""
<p style="margin:0 0 12px 0;font-size:15px;color:#14110f;">
  Hi <span {_ACCENT}>{name}</span>,
</p>
<p style="margin:0 0 20px 0;font-size:15px;color:#14110f;">
  This is a friendly reminder that you have an upcoming interview.
  Please review the details below and prepare accordingly.
</p>

<div {_CARD}>
  <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
    {_detail_row("💼", "Position", title)}
    {_detail_row("🏢", "Company", company)}
    {_detail_row("📅", "Date & Time", dt)}
    {_detail_row("📍", "Mode", mode)}
  </table>
</div>

<p style="margin:20px 0 0 0;font-size:15px;color:#14110f;">
  <span {_BADGE}>⏰ Interview in {(app.interview_at.date() - today).days} day(s)</span>
</p>

<p {_MUTED}>
  Good luck! Make sure to keep your resume and any relevant documents ready.
</p>
"""
            send_email(
                app.student.user.email,
                "📋 Upcoming Interview Reminder",
                body,
                text=f"Interview reminder: {title} at {company} on {dt}",
            )
            count += 1
    return count


def _deadline_reminders() -> int:
    today = date.today()
    horizon = today + timedelta(days=current_app.config.get("REMINDER_DEADLINE_DAYS", 3))
    count = 0
    drives = PlacementDrive.query.filter(
        PlacementDrive.status == DriveStatus.APPROVED,
        PlacementDrive.deadline >= today,
        PlacementDrive.deadline <= horizon,
    ).all()
    students = StudentProfile.query.all()
    for drive in drives:
        applied = {a.student_id for a in drive.applications}
        for student in students:
            if student.id in applied or eligibility_reasons(student, drive) or not student.user:
                continue

            name = student.name or "Student"
            title = drive.job_title
            company = drive.company.company_name
            dl = drive.deadline.strftime("%d %B %Y")
            days_left = (drive.deadline - today).days
            pkg = f"₹{drive.package_lpa} LPA" if drive.package_lpa else "Not disclosed"
            loc = drive.location or "—"
            skills = ", ".join(drive.skills_required) if drive.skills_required else "—"

            body = f"""
<p style="margin:0 0 12px 0;font-size:15px;color:#14110f;">
  Hi <span {_ACCENT}>{name}</span>,
</p>
<p style="margin:0 0 20px 0;font-size:15px;color:#14110f;">
  A placement drive you're eligible for is closing soon.
  Don't miss this opportunity — apply before the deadline!
</p>

<div {_CARD}>
  <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
    {_detail_row("💼", "Role", title)}
    {_detail_row("🏢", "Company", company)}
    {_detail_row("💰", "Package", pkg)}
    {_detail_row("📍", "Location", loc)}
    {_detail_row("🛠️", "Skills", skills)}
    {_detail_row("📅", "Deadline", dl)}
  </table>
</div>

<p style="margin:20px 0 0 0;font-size:15px;color:#14110f;">
  <span {_BADGE}>⚡ {days_left} day(s) remaining</span>
</p>

<p {_MUTED}>
  Log in to PlaceMint to review the full job description and submit your application.
</p>
"""
            send_email(
                student.user.email,
                "⏰ Application Deadline Approaching",
                body,
                text=f"Deadline reminder: {title} at {company} closes {dl}",
            )
            count += 1
    return count


def run_daily_reminders() -> dict:
    return {"interviews": _interview_reminders(), "deadlines": _deadline_reminders()}


@shared_task(name="app.tasks.reminders.send_daily_reminders")
def send_daily_reminders() -> dict:
    return run_daily_reminders()


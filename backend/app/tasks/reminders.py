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


def _interview_reminders() -> int:
    today = date.today()
    horizon = today + timedelta(days=2)
    count = 0
    for app in Application.query.filter(Application.interview_at.isnot(None)).all():
        if today <= app.interview_at.date() <= horizon and app.student and app.student.user:
            send_email(
                app.student.user.email, "Upcoming interview reminder",
                f"<p>Your interview for <strong>{app.drive.job_title}</strong> at "
                f"{app.drive.company.company_name} is on {app.interview_at:%d %b %Y %H:%M}.</p>",
                text="Interview reminder",
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
            send_email(
                student.user.email, "Application deadline approaching",
                f"<p>{drive.job_title} at {drive.company.company_name} closes on "
                f"{drive.deadline}. You are eligible, so apply before it closes.</p>",
                text="Deadline reminder",
            )
            count += 1
    return count


def run_daily_reminders() -> dict:
    return {"interviews": _interview_reminders(), "deadlines": _deadline_reminders()}


@shared_task(name="app.tasks.reminders.send_daily_reminders")
def send_daily_reminders() -> dict:
    return run_daily_reminders()

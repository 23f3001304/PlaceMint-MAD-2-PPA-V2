"""Celery task for sending asynchronous emails."""
from celery import shared_task
from app.utils.email import send_email


@shared_task(name="app.tasks.mail.send_email_task")
def send_email_task(to, subject: str, html: str, text: str | None = None) -> None:
    send_email(to, subject, html, text=text)

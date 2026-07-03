"""Email sending with a console backend for dev and SMTP for production.

`MAIL_BACKEND=console` (the default) logs the message instead of sending, so the
whole app runs with no mail server during development and demos.
"""
import smtplib
from email.message import EmailMessage

from flask import current_app


def _recipients(to) -> str:
    return to if isinstance(to, str) else ", ".join(to)


def send_email(to, subject: str, html: str, text: str | None = None) -> None:
    cfg = current_app.config
    if cfg.get("MAIL_BACKEND", "console") == "console":
        current_app.logger.info(
            "[email] to=%s subject=%s\n%s", _recipients(to), subject, text or "(html body)"
        )
        return

    message = EmailMessage()
    message["From"] = cfg["MAIL_FROM"]
    message["To"] = _recipients(to)
    message["Subject"] = subject
    message.set_content(text or "This message requires an HTML-capable client.")
    message.add_alternative(html, subtype="html")

    with smtplib.SMTP(cfg["SMTP_HOST"], cfg["SMTP_PORT"]) as server:
        server.starttls()
        if cfg.get("SMTP_USER"):
            server.login(cfg["SMTP_USER"], cfg["SMTP_PASSWORD"])
        server.send_message(message)

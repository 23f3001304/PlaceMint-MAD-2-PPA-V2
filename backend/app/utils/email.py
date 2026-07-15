"""Email sending with a console backend for dev and SMTP for production.

`MAIL_BACKEND=console` (the default) logs the message instead of sending, so the
whole app runs with no mail server during development and demos.
"""
import smtplib
from email.message import EmailMessage

from flask import current_app


def _recipients(to) -> str:
    return to if isinstance(to, str) else ", ".join(to)


def wrap_html_template(subject: str, body_html: str) -> str:
    has_h2 = "h2" in body_html.lower() or "<h2" in body_html.lower()
    title_html = f"<h2>{subject}</h2>" if not has_h2 else ""
    return f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{subject}</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@700&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap');
    body {{
      font-family: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      background-color: #f4f0e8;
      color: #14110f;
      margin: 0;
      padding: 0;
      -webkit-font-smoothing: antialiased;
    }}
    .wrapper {{
      width: 100%;
      background-color: #f4f0e8;
      padding: 40px 20px;
      box-sizing: border-box;
    }}
    .container {{
      max-width: 600px;
      margin: 0 auto;
      background-color: #ffffff;
      border: 1px solid rgba(20, 17, 15, 0.1);
      border-radius: 12px;
      overflow: hidden;
      box-shadow: 0 4px 12px rgba(20, 17, 15, 0.03);
    }}
    .header {{
      background-color: #1f6b3a;
      padding: 32px 40px;
      text-align: left;
      border-bottom: 4px solid #14472a;
    }}
    .logo {{
      font-family: 'Bricolage Grotesque', 'IBM Plex Sans', sans-serif;
      font-size: 28px;
      font-weight: 700;
      color: #efe9dc;
      margin: 0;
      letter-spacing: -0.5px;
    }}
    .logo span {{
      color: #efe9dc;
      opacity: 0.8;
      font-weight: 400;
    }}
    .content {{
      padding: 40px;
      line-height: 1.6;
      font-size: 16px;
    }}
    .content h2 {{
      font-family: 'Bricolage Grotesque', sans-serif;
      color: #1f6b3a;
      font-size: 22px;
      margin-top: 0;
      margin-bottom: 16px;
    }}
    .content p {{
      margin-top: 0;
      margin-bottom: 20px;
      color: #14110f;
    }}
    .content strong {{
      color: #1f6b3a;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      background-color: #faf8f5;
      margin: 20px 0;
      border: 1px solid rgba(20, 17, 15, 0.08);
      border-radius: 8px;
    }}
    th, td {{
      padding: 12px 16px;
      text-align: left;
      border-bottom: 1px solid rgba(20, 17, 15, 0.08);
      font-size: 15px;
    }}
    tr:last-child td {{
      border-bottom: none;
    }}
    .footer {{
      background-color: #faf8f5;
      padding: 24px 40px;
      text-align: center;
      border-top: 1px solid rgba(20, 17, 15, 0.08);
      font-size: 13px;
      color: #6b6357;
    }}
    .footer p {{
      margin: 4px 0;
    }}
  </style>
</head>
<body>
  <div class="wrapper">
    <div class="container">
      <div class="header">
        <h1 class="logo">Place<span>Mint</span></h1>
      </div>
      <div class="content">
        {title_html}
        {body_html}
      </div>
      <div class="footer">
        <p>This is an automated message from the PlaceMint Campus Recruitment Cell.</p>
        <p>&copy; 2026 Mint University. All rights reserved.</p>
      </div>
    </div>
  </div>
</body>
</html>
"""


def send_email(to, subject: str, html: str, text: str | None = None) -> None:
    cfg = current_app.config
    if cfg.get("MAIL_BACKEND", "console") == "console":
        current_app.logger.info(
            "[email] to=%s subject=%s\n%s", _recipients(to), subject, text or "(html body)"
        )
        return

    # Wrap standard content in our beautiful template
    if not html.strip().startswith("<!DOCTYPE html>"):
        html = wrap_html_template(subject, html)

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

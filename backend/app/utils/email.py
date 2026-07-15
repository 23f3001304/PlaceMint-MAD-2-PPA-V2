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
    """Wrap body_html in the PlaceMint branded email shell.

    Uses fully inlined styles so the design survives Gmail, Outlook and
    every other client that strips ``<style>`` blocks.
    """
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{subject}</title>
  <!--[if mso]>
  <noscript><xml>
    <o:OfficeDocumentSettings><o:PixelsPerInch>96</o:PixelsPerInch></o:OfficeDocumentSettings>
  </xml></noscript>
  <![endif]-->
</head>
<body style="margin:0;padding:0;background-color:#f4f0e8;font-family:'IBM Plex Sans',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;color:#14110f;-webkit-font-smoothing:antialiased;">

  <!-- Outer wrapper -->
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"
         style="background-color:#f4f0e8;padding:40px 0;">
    <tr>
      <td align="center">

        <!-- Container card -->
        <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0"
               style="max-width:600px;width:100%;background-color:#ffffff;border-radius:12px;overflow:hidden;border:1px solid rgba(20,17,15,0.10);box-shadow:0 4px 24px rgba(20,17,15,0.06);">

          <!-- ======= HEADER ======= -->
          <tr>
            <td style="background:linear-gradient(135deg,#1f6b3a 0%,#176030 100%);padding:28px 40px;border-bottom:4px solid #14472a;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td>
                    <h1 style="margin:0;font-family:'Bricolage Grotesque','IBM Plex Sans',sans-serif;font-size:26px;font-weight:700;color:#efe9dc;letter-spacing:-0.5px;">
                      Place<span style="opacity:0.75;font-weight:400;">Mint</span>
                    </h1>
                    <p style="margin:4px 0 0 0;font-size:13px;color:rgba(239,233,220,0.7);letter-spacing:0.3px;">
                      Campus Recruitment Cell
                    </p>
                  </td>
                  <td align="right" valign="middle">
                    <span style="display:inline-block;width:38px;height:38px;border-radius:50%;background-color:rgba(239,233,220,0.15);text-align:center;line-height:38px;font-size:18px;">
                      🎓
                    </span>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- ======= SUBJECT BAR ======= -->
          <tr>
            <td style="padding:24px 40px 0 40px;">
              <h2 style="margin:0;font-family:'Bricolage Grotesque','IBM Plex Sans',sans-serif;font-size:21px;font-weight:700;color:#1f6b3a;line-height:1.3;">
                {subject}
              </h2>
              <hr style="border:none;border-top:2px solid #e8e3d8;margin:16px 0 0 0;">
            </td>
          </tr>

          <!-- ======= BODY CONTENT ======= -->
          <tr>
            <td style="padding:24px 40px 32px 40px;font-size:15px;line-height:1.65;color:#14110f;">
              {body_html}
            </td>
          </tr>

          <!-- ======= FOOTER ======= -->
          <tr>
            <td style="background-color:#faf8f5;padding:20px 40px;border-top:1px solid rgba(20,17,15,0.08);text-align:center;">
              <p style="margin:0 0 4px 0;font-size:12px;color:#6b6357;">
                This is an automated message from the PlaceMint Placement Portal.
              </p>
              <p style="margin:0;font-size:12px;color:#9b9589;">
                &copy; 2026 Mint University &middot; All rights reserved
              </p>
            </td>
          </tr>

        </table>
        <!-- /Container card -->

      </td>
    </tr>
  </table>
  <!-- /Outer wrapper -->

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

    # Wrap standard content in our branded template
    if not html.strip().lower().startswith("<!doctype"):
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


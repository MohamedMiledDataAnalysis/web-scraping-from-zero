"""Send an alert email. Settings come from environment variables."""

import os
import smtplib
from email.message import EmailMessage


def send_alert(subject, body):
    host = os.environ.get("ALERT_SMTP_HOST", "localhost")
    port = int(os.environ.get("ALERT_SMTP_PORT", "1025"))
    user = os.environ.get("ALERT_SMTP_USER")
    password = os.environ.get("ALERT_SMTP_PASSWORD")
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = os.environ.get("ALERT_FROM", "scraper@localhost")
    msg["To"] = os.environ.get("ALERT_TO", "me@localhost")
    msg.set_content(body)
    with smtplib.SMTP(host, port, timeout=30) as smtp:
        if user:  # a real mail server: encrypt, then log in
            smtp.starttls()
            smtp.login(user, password)
        smtp.send_message(msg)

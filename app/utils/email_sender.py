import os
import smtplib
from email.mime.text import MIMEText

def send_email(to_email: str, subject: str, body: str):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    sender_email = os.getenv("EMAIL_USER")
    sender_password = os.getenv("EMAIL_PASS")

    if not sender_email or not sender_password:
        raise Exception("Email credentials not found in environment variables.")

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())

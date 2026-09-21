# app/services/email_service.py

import smtplib
from email.mime.text import MIMEText
from fastapi import HTTPException


SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "selemaniseif1974@gmail.com"
SMTP_PASSWORD = "fgzpiqpsftuzmtdm"   # your app password


def send_email(email_to: str, subject: str, body: str):
    """
    Reusable email sender for any part of the backend.
    Used by:
    - payment webhook (send token to user)
    - admin notifications
    - future automated systems
    """

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = email_to

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, [email_to], msg.as_string())
        server.quit()
    except Exception as e:
        print("Email sending failed:", e)
        raise HTTPException(status_code=500, detail="Failed to send email.")

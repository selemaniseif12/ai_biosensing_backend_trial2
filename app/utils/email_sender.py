import os
import requests

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDGRID_URL = "https://api.sendgrid.com/v3/mail/send"


def send_email(to_email: str, subject: str, body: str):
    if not SENDGRID_API_KEY:
        raise Exception("SENDGRID_API_KEY is missing from environment variables.")

    payload = {
        "personalizations": [
            {
                "to": [{"email": to_email}],
                "subject": subject
            }
        ],
        "from": {"email": "selemaniseif12@yahoo.com"},  # ⭐ VERIFIED SENDER
        "content": [
            {
                "type": "text/plain",
                "value": body
            }
        ]
    }

    headers = {
        "Authorization": f"Bearer {SENDGRID_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(SENDGRID_URL, json=payload, headers=headers)

    if response.status_code >= 400:
        raise Exception(f"SendGrid error: {response.status_code} - {response.text}")

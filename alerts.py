# scripts/alerts.py

from twilio.rest import Client
from dotenv import load_dotenv
import os



# Load environment variables from .env
load_dotenv()

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_PHONE")
ALERT_PHONE = os.getenv("ALERT_PHONE")


def send_sms_alert(message):
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    msg = client.messages.create(
        body=message,
        from_=TWILIO_PHONE,
        to=ALERT_PHONE
    )
    print("📨 SMS Sent:", msg.sid)

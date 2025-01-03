from twilio.rest import Client
from django.conf import settings

def send_sms_func(phone_number, body):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    message = client.messages.create(
        body=body,
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone_number
    )

    return message.sid

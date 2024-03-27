# vehiapp/utils.py

from twilio.rest import Client
from django.conf import settings

def send_otp(phone_number, otp):
    # Initialize Twilio client
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    
    try:
        # Send SMS message with OTP
        message = client.messages.create(
            to=phone_number,
            from_=settings.TWILIO_PHONE_NUMBER,
            body=f'Your OTP is: {otp}'
        )
        print(f"OTP sent successfully to {phone_number}")
        return True
    except Exception as e:
        print(f"Error sending OTP to {phone_number}: {e}")
        return False


# vehiapp/utils.py

import random

def generate_otp():
    return str(random.randint(1000, 9999))

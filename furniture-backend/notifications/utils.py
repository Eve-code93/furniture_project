# notifications/utils.py
from django.core.mail import send_mail
from django.utils import timezone

def send_whatsapp_message_demo(phone_number, message):
    # Replace with real provider like Twilio / Meta WhatsApp API
    # This is a synchronous demo wrapper — used by Celery task.
    print(f"[WHATSAPP DEMO] to {phone_number}: {message}")
    return True

def send_sms_message_demo(phone_number, message):
    print(f"[SMS DEMO] to {phone_number}: {message}")
    return True

def send_email_message(subject, message, recipient_email):
    # Uses Django's send_mail — ensure EMAIL_* settings are configured
    send_mail(subject or "Notification", message, None, [recipient_email], fail_silently=False)
    return True

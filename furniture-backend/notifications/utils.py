# notifications/utils.py
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from accounts.models import User  # or your actual user model if custom
from django.core.mail import send_mail

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
def notify_admins_low_stock(inventory):
    """
    Notify all staff users that a product is low in stock.
    """
    subject = f"Low Stock Alert: {inventory.product.name}"
    message = f"Remaining stock for {inventory.product.name} is {inventory.remaining}."
    admin_emails = User.objects.filter(is_staff=True).values_list('email', flat=True)
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, admin_emails)


def notify_clients_product_available(product):
    """
    Notify clients who subscribed to restock alerts for this product.
    """
    # You can implement a RestockAlert model if you like
    # For now, we'll just print to console as a placeholder
    print(f"Notify clients: {product.name} is back in stock!")

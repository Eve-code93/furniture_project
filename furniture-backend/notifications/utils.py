from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from accounts.models import User  # or your custom user model

# -------------------------------
# WhatsApp / SMS Demo Functions
# -------------------------------

def send_whatsapp_message_demo(phone_number, message):
    # Replace with real provider like Twilio / Meta WhatsApp API
    print(f"[WHATSAPP DEMO] to {phone_number}: {message}")
    return True

def send_sms_message_demo(phone_number, message):
    print(f"[SMS DEMO] to {phone_number}: {message}")
    return True

def send_email_message(subject, message, recipient_email):
    send_mail(subject or "Notification", message, None, [recipient_email], fail_silently=False)
    return True

# -------------------------------
# Inventory Notifications
# -------------------------------

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
    # You can implement a RestockAlert model if needed
    print(f"Notify clients: {product.name} is back in stock!")

# -------------------------------
# Promotions / Coupons
# -------------------------------

def notify_admins_promotion(promo):
    subject = f"New Promotion: {promo.name}"
    message = f"Promotion '{promo.name}' ({promo.promo_type} - {promo.value}) is now active."
    admin_emails = User.objects.filter(is_staff=True).values_list('email', flat=True)
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, admin_emails)

def notify_admins_coupon(coupon):
    subject = f"New Coupon: {coupon.code}"
    message = f"Coupon '{coupon.code}' ({coupon.discount_type} - {coupon.value}) is now active."
    admin_emails = User.objects.filter(is_staff=True).values_list('email', flat=True)
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, admin_emails)

# payments/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Payment
from notifications.utils import send_email_message, send_whatsapp_message_demo, send_sms_message_demo
from accounts.models import User  # or your actual user model if custom


@receiver(post_save, sender=Payment)
def payment_post_save(sender, instance, created, **kwargs):
    """
    Sends notifications to admins and optionally customers
    whenever a payment is marked success or failed.
    """
    if created:
        # New payment created
        if instance.status == instance.PaymentStatus.SUCCESS:
            subject = f"Payment Received - Order #{instance.order.id}"
            message = f"Payment of {instance.amount} via {instance.method} was successful for Order #{instance.order.id}."
            notify_admins_payment(instance, subject, message)
        elif instance.status == instance.PaymentStatus.FAILED:
            subject = f"Payment Failed - Order #{instance.order.id}"
            message = f"Payment of {instance.amount} via {instance.method} failed for Order #{instance.order.id}."
            notify_admins_payment(instance, subject, message)


def notify_admins_payment(payment, subject, message):
    """
    Notify all admin users about payment status via email, SMS, or WhatsApp.
    """
    admin_users = User.objects.filter(is_staff=True)
    for admin in admin_users:
        if admin.email:
            send_email_message(subject, message, admin.email)
        if hasattr(admin, "phone") and admin.phone:
            send_sms_message_demo(admin.phone, message)
            send_whatsapp_message_demo(admin.phone, message)

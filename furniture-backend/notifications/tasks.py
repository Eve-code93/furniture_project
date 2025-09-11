# notifications/tasks.py
from celery import shared_task
from django.utils import timezone
from django.conf import settings
from .models import Notification, NotificationPreference
from .utils import send_whatsapp_message_demo, send_sms_message_demo, send_email_message

@shared_task(bind=True, max_retries=3, default_retry_delay=10)
def send_notification_task(self, notification_id):
    """
    Celery task: pick up Notification by id and attempt to send.
    The Notification row should already exist in DB.
    """
    try:
        notif = Notification.objects.select_related('user').get(pk=notification_id)
    except Notification.DoesNotExist:
        return {'status': 'not_found', 'id': notification_id}

    user = notif.user

    # Check global preference (create default if missing)
    prefs, _ = NotificationPreference.objects.get_or_create(user=user)

    if not prefs.allow_notifications:
        return {'status': 'blocked_by_user', 'id': notification_id}

    channel = notif.channel

    try:
        if channel == 'whatsapp':
            phone = getattr(user, 'phone', None) or getattr(user, 'phone_number', None)
            if not phone:
                notif.sent = False
                notif.save()
                return {'status': 'no_phone', 'id': notification_id}
            if not prefs.allow_whatsapp:
                return {'status': 'channel_disabled', 'id': notification_id}
            ok = send_whatsapp_message_demo(phone, notif.message)
        elif channel == 'sms':
            phone = getattr(user, 'phone', None) or getattr(user, 'phone_number', None)
            if not phone:
                notif.sent = False
                notif.save()
                return {'status': 'no_phone', 'id': notification_id}
            if not prefs.allow_sms:
                return {'status': 'channel_disabled', 'id': notification_id}
            ok = send_sms_message_demo(phone, notif.message)
        elif channel == 'email':
            email = getattr(user, 'email', None)
            if not email:
                notif.sent = False
                notif.save()
                return {'status': 'no_email', 'id': notification_id}
            if not prefs.allow_email:
                return {'status': 'channel_disabled', 'id': notification_id}
            ok = send_email_message(notif.title, notif.message, email)
        elif channel == 'in_app':
            # in-app is just a DB record — nothing else to do
            ok = True
        else:
            ok = False

        if ok:
            notif.sent = True
            notif.sent_at = timezone.now()
            notif.save()
            return {'status': 'sent', 'id': notification_id}
        else:
            notif.sent = False
            notif.save()
            return {'status': 'failed_send', 'id': notification_id}

    except Exception as exc:
        try:
            self.retry(exc=exc)
        except self.MaxRetriesExceededError:
            notif.sent = False
            notif.save()
            return {'status': 'failed_max_retries', 'id': notification_id}

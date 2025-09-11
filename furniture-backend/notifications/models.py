# notifications/models.py
from django.db import models
from django.conf import settings

class NotificationPreference(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notification_preferences"
    )
    allow_whatsapp = models.BooleanField(default=True)
    allow_email = models.BooleanField(default=True)
    allow_sms = models.BooleanField(default=False)
    allow_in_app = models.BooleanField(default=True)
    allow_notifications = models.BooleanField(default=True)

    def __str__(self):
        return f"Prefs for {self.user}"


class Notification(models.Model):
    CHANNEL_CHOICES = (
        ('whatsapp', 'WhatsApp'),
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('in_app', 'In-App'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )
    title = models.CharField(max_length=255, blank=True)
    message = models.TextField()
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES)
    sent = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.channel} to {self.user}: {self.message[:30]}"

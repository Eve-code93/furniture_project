# notifications/serializers.py
from rest_framework import serializers
from .models import Notification, NotificationPreference


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for Notification objects."""
    
    class Meta:
        model = Notification
        fields = [
            'id',
            'user',
            'channel',
            'message',
            'sent',
            'is_read',
            'created_at',
            'sent_at',
        ]
        read_only_fields = ['id', 'user', 'sent', 'created_at', 'sent_at']


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    """Serializer for managing user notification preferences."""

    class Meta:
        model = NotificationPreference
        fields = [
            'allow_whatsapp',
            'allow_email',
            'allow_sms',
            'allow_in_app',
            'allow_notifications',
        ]

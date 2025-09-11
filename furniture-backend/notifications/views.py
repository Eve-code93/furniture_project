# notifications/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Notification, NotificationPreference
from .serializers import NotificationSerializer, NotificationPreferenceSerializer
from .tasks import send_notification_task

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Notification.objects.all().order_by('-created_at')
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')


class NotificationPreferenceView(generics.RetrieveUpdateAPIView):
    serializer_class = NotificationPreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj, _ = NotificationPreference.objects.get_or_create(user=self.request.user)
        return obj


class SendNotificationView(APIView):
    """
    POST to create a Notification and enqueue the task.
    body: { "channel": "whatsapp"|"email"|"sms"|"in_app", "title": "...", "message": "..." }
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        channel = request.data.get('channel')
        message = request.data.get('message')
        title = request.data.get('title', '')

        if not channel or not message:
            return Response({"detail": "channel and message required"}, status=status.HTTP_400_BAD_REQUEST)

        if channel not in dict(Notification.CHANNEL_CHOICES).keys():
            return Response({"detail": "invalid channel"}, status=status.HTTP_400_BAD_REQUEST)

        # Create Notification record
        notif = Notification.objects.create(
            user=request.user,
            title=title,
            message=message,
            channel=channel
        )

        # Enqueue Celery task (async)
        send_notification_task.delay(notif.id)

        serializer = NotificationSerializer(notif)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# notifications/urls.py
from django.urls import path
from .views import NotificationListView, NotificationPreferenceView, SendNotificationView

urlpatterns = [
    path('', NotificationListView.as_view(), name='notifications-list'),
    path('preferences/', NotificationPreferenceView.as_view(), name='notification-preferences'),
    path('send/', SendNotificationView.as_view(), name='notification-send'),
]

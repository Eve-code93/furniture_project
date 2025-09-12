from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, OrderStatusHistory

try:
    from notifications import NotificationHandler
except ImportError:
    class NotificationHandler:
        @staticmethod
        def notify(user, title, message):
            print(f"[Notify {user}] {title}: {message}")


@receiver(post_save, sender=Order)
def create_status_history_and_notify(sender, instance, created, **kwargs):
    if created:
        # Initial history record
        OrderStatusHistory.objects.create(
            order=instance,
            status=instance.status,
            note="Order created"
        )
        NotificationHandler.notify(
            instance.customer,
            "Order Created",
            f"Your order #{instance.id} has been created."
        )
    else:
        # Check last status in history
        last_history = instance.status_history.last()
        if not last_history or last_history.status != instance.status:
            OrderStatusHistory.objects.create(
                order=instance,
                status=instance.status,
                note=f"Status updated to {instance.status}"
            )
            NotificationHandler.notify(
                instance.customer,
                "Order Status Changed",
                f"Your order #{instance.id} is now {instance.status}."
            )
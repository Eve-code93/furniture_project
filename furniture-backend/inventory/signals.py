# inventory/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Inventory
from notifications.utils import notify_admins_low_stock, notify_clients_product_available

@receiver(post_save, sender=Inventory)
def inventory_stock_alert(sender, instance: Inventory, created, **kwargs):
    """
    Trigger notifications:
    - To admins if stock is low
    - To clients if stock was zero and now restocked
    """
    # Notify admins if stock is low
    if instance.is_low_stock():
        notify_admins_low_stock(instance)

    # Notify clients if product was out of stock and now restocked
    if not created:
        # Fetch previous stock from database
        previous = Inventory.objects.get(pk=instance.pk)
        if previous.remaining == 0 and instance.remaining > 0:
            notify_clients_product_available(instance.product)

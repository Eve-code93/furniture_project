from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Promotion, Coupon
from notifications.utils import notify_admins_promotion, notify_admins_coupon

@receiver(post_save, sender=Promotion)
def promotion_post_save(sender, instance, created, **kwargs):
    """
    Notify admins when a new promotion is created.
    """
    if created:
        notify_admins_promotion(instance)

@receiver(post_save, sender=Coupon)
def coupon_post_save(sender, instance, created, **kwargs):
    """
    Notify admins when a new coupon is created.
    """
    if created:
        notify_admins_coupon(instance)

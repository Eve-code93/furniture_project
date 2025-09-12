from django.db import models
from django.utils import timezone
from products.models import Product, Category
from decimal import Decimal


class Promotion(models.Model):
    """
    Promotion that can be applied to products or categories.
    Can be percentage-based or fixed-amount discounts.
    """
    PERCENTAGE = 'percentage'
    FIXED = 'fixed'
    PROMO_TYPE_CHOICES = [
        (PERCENTAGE, 'Percentage Discount'),
        (FIXED, 'Fixed Amount Discount'),
    ]

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    promo_type = models.CharField(max_length=20, choices=PROMO_TYPE_CHOICES)
    value = models.DecimalField(max_digits=10, decimal_places=2, help_text="Percentage (0-100) or fixed amount")
    active = models.BooleanField(default=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)

    products = models.ManyToManyField(Product, blank=True, related_name="promotions")
    categories = models.ManyToManyField(Category, blank=True, related_name="promotions")

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.name} ({self.promo_type} - {self.value})"

    def is_active_now(self):
        now = timezone.now()
        return self.active and self.start_date <= now and (self.end_date is None or now <= self.end_date)


class Coupon(models.Model):
    """
    Coupon code that users can apply at checkout.
    Tracks usage limits and status.
    """
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    discount_type = models.CharField(max_length=20, choices=Promotion.PROMO_TYPE_CHOICES)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)
    usage_limit = models.PositiveIntegerField(null=True, blank=True, help_text="Maximum times it can be used")
    used_count = models.PositiveIntegerField(default=0)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.code} ({self.discount_type} - {self.value})"

    def can_use(self):
        now = timezone.now()
        if not self.active or (self.start_date and self.start_date > now) or (self.end_date and now > self.end_date):
            return False
        if self.usage_limit is not None and self.used_count >= self.usage_limit:
            return False
        return True

    def mark_used(self):
        self.used_count += 1
        self.save(update_fields=['used_count'])

from decimal import Decimal
from django.conf import settings
from django.db import models
from products.models import Product, ProductVariant

User = settings.AUTH_USER_MODEL


class Order(models.Model):
    PENDING = 'pending'
    PROCESSING = 'processing'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (PROCESSING, 'Processing'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
        (CANCELLED, 'Cancelled'),
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    shipping_cost = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))

    shipping_address = models.TextField(blank=True, null=True)
    delivery_instructions = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} by {self.customer}"

    def recalc_total(self):
        total = Decimal('0.00')
        for item in self.items.all():
            total += item.total_price
        self.total_price = (total + self.shipping_cost - self.discount_amount).quantize(Decimal("0.01"))
        self.save(update_fields=['total_price', 'updated_at'])


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    variant = models.ForeignKey(ProductVariant, null=True, blank=True, on_delete=models.SET_NULL)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']
        unique_together = ('order', 'product', 'variant')

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def set_prices_from_product(self):
        if self.variant and self.variant.price_override is not None:
            price = self.variant.price_override
        else:
            price = self.product.sale_price if self.product.sale_price else self.product.base_price
        self.unit_price = Decimal(price).quantize(Decimal("0.01"))
        self.total_price = (self.unit_price * Decimal(self.quantity)).quantize(Decimal("0.01"))

    def save(self, *args, **kwargs):
        self.set_prices_from_product()
        super().save(*args, **kwargs)


class OrderStatusHistory(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="status_history")
    status = models.CharField(max_length=20, choices=Order.STATUS_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Order #{self.order.id} - {self.status} at {self.timestamp}"

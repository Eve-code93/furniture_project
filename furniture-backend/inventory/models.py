from django.db import models
from django.conf import settings
from products.models import Product, Category

User = settings.AUTH_USER_MODEL


class Inventory(models.Model):
    """
    Track stock levels per product.
    Shows sold, remaining, and low-stock alerts.
    """
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name="inventory"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="inventories"
    )
    total_stock = models.PositiveIntegerField(default=0)
    sold = models.PositiveIntegerField(default=0)
    remaining = models.PositiveIntegerField(default=0)
    reorder_threshold = models.PositiveIntegerField(
        default=5,
        help_text="Trigger low-stock alert when remaining <= this number"
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - Remaining: {self.remaining}"

    def is_low_stock(self):
        return self.remaining <= self.reorder_threshold

    def adjust_stock(self, quantity: int, action="sale"):
        """
        Adjust stock levels.
        - action='sale' for reducing stock
        - action='restock' for adding stock
        """
        if action == "sale":
            self.sold += abs(quantity)
            self.remaining = max(0, self.remaining - abs(quantity))
        elif action == "restock":
            self.total_stock += quantity
            self.remaining += quantity

        self.save(update_fields=["sold", "remaining", "total_stock", "updated_at"])
        return self.remaining

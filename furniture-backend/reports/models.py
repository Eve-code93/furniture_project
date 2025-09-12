# reports/models.py
from django.db import models
from django.utils import timezone
from inventory.models import Inventory
from order_management.models import Order
from payments.models import Payment

class SalesReport(models.Model):
    """
    Daily summary of sales and payments.
    """
    date = models.DateField(default=timezone.now, unique=True)
    total_orders = models.PositiveIntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_payments = models.PositiveIntegerField(default=0)
    total_refunds = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Sales Report - {self.date}"


class InventoryReport(models.Model):
    """
    Daily summary of inventory stock levels.
    """
    date = models.DateField(default=timezone.now, unique=True)
    low_stock_items = models.PositiveIntegerField(default=0)
    total_stock = models.PositiveIntegerField(default=0)
    sold_items = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Inventory Report - {self.date}"

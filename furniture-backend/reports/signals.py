# reports/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from order_management.models import Order
from inventory.models import Inventory
from .models import SalesReport, InventoryReport
from payments.models import Payment

@receiver(post_save, sender=Order)
def update_sales_report(sender, instance, created, **kwargs):
    today = timezone.now().date()
    report, _ = SalesReport.objects.get_or_create(date=today)
    orders_today = Order.objects.filter(created_at__date=today)
    payments_today = Payment.objects.filter(created_at__date=today, status="success")
    
    report.total_orders = orders_today.count()
    report.total_revenue = sum([o.total_price for o in orders_today])
    report.total_payments = payments_today.count()
    report.total_refunds = sum([p.amount for p in payments_today if p.status == "refunded"])
    report.save(update_fields=['total_orders', 'total_revenue', 'total_payments', 'total_refunds'])


@receiver(post_save, sender=Inventory)
def update_inventory_report(sender, instance, created, **kwargs):
    today = timezone.now().date()
    report, _ = InventoryReport.objects.get_or_create(date=today)
    inventories = Inventory.objects.all()
    report.low_stock_items = sum([1 for i in inventories if i.is_low_stock()])
    report.total_stock = sum([i.total_stock for i in inventories])
    report.sold_items = sum([i.sold for i in inventories])
    report.save(update_fields=['low_stock_items', 'total_stock', 'sold_items'])

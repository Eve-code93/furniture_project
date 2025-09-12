from django.contrib import admin
from .models import SalesReport, InventoryReport

@admin.register(SalesReport)
class SalesReportAdmin(admin.ModelAdmin):
    list_display = ('date', 'total_orders', 'total_revenue', 'total_payments', 'total_refunds')
    ordering = ('-date',)

@admin.register(InventoryReport)
class InventoryReportAdmin(admin.ModelAdmin):
    list_display = ('date', 'low_stock_items', 'total_stock', 'sold_items')
    ordering = ('-date',)

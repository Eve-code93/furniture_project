from django.contrib import admin
from .models import Inventory


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'remaining', 'sold', 'total_stock', 'is_low_stock', 'updated_at')
    list_filter = ('category',)
    search_fields = ('product__name',)
    readonly_fields = ('remaining', 'sold', 'updated_at')

    def is_low_stock(self, obj):
        return obj.is_low_stock()
    is_low_stock.boolean = True

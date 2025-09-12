from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'customer', 'method', 'amount', 'status', 'transaction_id', 'created_at', 'confirmed_at')
    list_filter = ('status', 'method', 'created_at')
    search_fields = ('order__id', 'customer__username', 'transaction_id')

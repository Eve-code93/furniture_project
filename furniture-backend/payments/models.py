from django.db import models
from django.conf import settings
from django.utils import timezone
from order_management.models import Order

User = settings.AUTH_USER_MODEL


class PaymentMethod(models.TextChoices):
    MPESA = "mpesa", "M-Pesa"
    CARD = "card", "Credit/Debit Card"
    PAYPAL = "paypal", "PayPal"


class PaymentStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    SUCCESS = "success", "Success"
    FAILED = "failed", "Failed"
    REFUNDED = "refunded", "Refunded"


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payments")
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
    method = models.CharField(max_length=20, choices=PaymentMethod.choices)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    transaction_id = models.CharField(max_length=100, blank=True, null=True, help_text="Reference from gateway")
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.order} - {self.method} ({self.status})"

    def mark_success(self, transaction_id=None):
        self.status = PaymentStatus.SUCCESS
        if transaction_id:
            self.transaction_id = transaction_id
        self.confirmed_at = timezone.now()
        self.save(update_fields=["status", "transaction_id", "confirmed_at"])

    def mark_failed(self):
        self.status = PaymentStatus.FAILED
        self.save(update_fields=["status"])

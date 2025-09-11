from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer_profile")
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    delivery_instructions = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Customer: {self.user.name or self.user.email or self.user.phone}"

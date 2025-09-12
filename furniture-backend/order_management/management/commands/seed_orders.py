from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from order_management.models import Order, OrderItem, OrderStatusHistory
from products.models import Product
from django.utils import timezone
import random
from decimal import Decimal

User = get_user_model()

class Command(BaseCommand):
    help = "Seed the database with sample orders and order items"

    def handle(self, *args, **options):
        # ✅ Get or create a specific test user by email
        customer, created = User.objects.get_or_create(
            email="6EYQH@example.com",
            defaults={
                "name": "Seed Test User"
            }
        )
        if created:
            customer.set_password("testpassword123")
            customer.save()

        # ✅ Get some products to use in the orders
        products = list(Product.objects.all()[:5])
        if not products:
            self.stdout.write(self.style.ERROR("No products found. Add products first."))
            return

        for i in range(5):  # create 5 sample orders
            order = Order.objects.create(
                customer=customer,
                status=random.choice(['pending', 'processing', 'shipped', 'delivered']),
                shipping_address=f"123 Test Street, City {i}",
                delivery_instructions="Leave at front door",
                notes="Sample seeded order",
            )

            # Add 1-3 random items to each order
            total_price = Decimal("0.00")
            for j in range(random.randint(1, 3)):
                product = random.choice(products)
                quantity = random.randint(1, 5)
                price = Decimal(product.base_price)  # ✅ use your actual product price field
                total_price += price * quantity

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    unit_price=price,
                    total_price=price * quantity
                )

            order.total_price = total_price
            order.save()

            # Add a status history entry
            OrderStatusHistory.objects.create(
                order=order,
                status=order.status,
                note="Initial status",
                timestamp=timezone.now()
            )

        self.stdout.write(self.style.SUCCESS("✅ Successfully seeded sample orders."))

from django.core.management.base import BaseCommand
from products.models import Category, Product, ProductImage, ProductVariant, ProductVariantImage, Fabric
from django.utils.text import slugify
import random

class Command(BaseCommand):
    help = "Seed the database with sample categories, products, and variants"

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Seeding data..."))

        # --- Categories ---
        furniture = Category.objects.create(
            name="Furniture",
            slug="furniture",
            description="All kinds of furniture"
        )
        sofas = Category.objects.create(
            name="Sofas",
            slug="sofas",
            parent=furniture,
            description="Comfortable sofas"
        )
        tables = Category.objects.create(
            name="Tables",
            slug="tables",
            parent=furniture,
            description="Dining and coffee tables"
        )

        # --- Fabrics ---
        velvet = Fabric.objects.create(name="Velvet", description="Soft velvet fabric")
        linen = Fabric.objects.create(name="Linen", description="Natural linen fabric")

        # --- Products ---
        for i in range(3):
            product = Product.objects.create(
                name=f"Sample Sofa {i+1}",
                slug=slugify(f"sample-sofa-{i+1}"),
                sku=f"SOFA00{i+1}",
                description="A very comfy sample sofa",
                category=sofas,
                base_price=random.randint(1000, 3000),
                stock_quantity=10,
                color_family="Blue",
                style="Modern"
            )

            # Images
            ProductImage.objects.create(
                product=product,
                image="products/sample.jpg",
                alt_text="Sample sofa image",
                is_main=True
            )

            # Variants
            variant1 = ProductVariant.objects.create(
                product=product,
                name="Blue Velvet",
                sku=f"SOFA00{i+1}-VEL",
                price_override=product.base_price + 200,
                stock_quantity=5,
                fabric=velvet
            )
            ProductVariantImage.objects.create(
                variant=variant1,
                image="variants/sample-velvet.jpg",
                alt_text="Blue velvet sofa",
                is_main=True
            )

            variant2 = ProductVariant.objects.create(
                product=product,
                name="Beige Linen",
                sku=f"SOFA00{i+1}-LIN",
                price_override=product.base_price + 100,
                stock_quantity=8,
                fabric=linen
            )
            ProductVariantImage.objects.create(
                variant=variant2,
                image="variants/sample-linen.jpg",
                alt_text="Beige linen sofa",
                is_main=True
            )

        self.stdout.write(self.style.SUCCESS("✅ Sample data seeded successfully!"))

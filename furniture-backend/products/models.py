from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# --------------------------
# CATEGORY / SPACES
# --------------------------
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subcategories')
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='categories/', null=True, blank=True)

    meta_title = models.CharField(max_length=150, blank=True)
    meta_description = models.CharField(max_length=300, blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name


# --------------------------
# FABRIC LIBRARY (Optional)
# --------------------------
class Fabric(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    sample_image = models.ImageField(upload_to='fabrics/', null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# --------------------------
# PRODUCT
# --------------------------
class Product(models.Model):
    READY_MADE = 'ready'
    CUSTOM_MADE = 'custom'
    PRODUCT_TYPE_CHOICES = [
        (READY_MADE, 'Ready Made'),
        (CUSTOM_MADE, 'Custom Made'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    sku = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    collection = models.CharField(max_length=100, blank=True)

    product_type = models.CharField(max_length=10, choices=PRODUCT_TYPE_CHOICES, default=READY_MADE)

    base_price = models.DecimalField(max_digits=12, decimal_places=2)
    sale_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    cost_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    stock_quantity = models.IntegerField(default=0)
    low_stock_threshold = models.IntegerField(default=5)
    track_inventory = models.BooleanField(default=True)

    production_time_days = models.IntegerField(null=True, blank=True)
    requires_approval = models.BooleanField(default=False)

    dimensions_cm = models.CharField(max_length=50, blank=True)

    primary_material = models.CharField(max_length=100, blank=True)
    color_family = models.CharField(max_length=50, blank=True)
    style = models.CharField(max_length=50, blank=True)

    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_bestseller = models.BooleanField(default=False)
    is_new_arrival = models.BooleanField(default=False)
    show_in_catalog = models.BooleanField(default=True)

    supports_customization = models.BooleanField(default=False)
    custom_request_instructions = models.TextField(blank=True)

    care_instructions = models.TextField(blank=True)
    warranty_months = models.IntegerField(null=True, blank=True)
    assembly_required = models.BooleanField(default=False)
    assembly_time_minutes = models.IntegerField(null=True, blank=True)

    instagram_caption = models.TextField(blank=True)
    hashtags = models.CharField(max_length=300, blank=True)

    meta_title = models.CharField(max_length=150, blank=True)
    meta_description = models.CharField(max_length=300, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=150, blank=True)
    is_main = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order']

    def __str__(self):
        return f"{self.product.name} Image"


# --------------------------
# PRODUCT VARIANTS
# --------------------------
class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=50, unique=True)
    price_override = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    stock_quantity = models.IntegerField(default=0)
    fabric = models.ForeignKey(Fabric, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        unique_together = ('product', 'name')

    def __str__(self):
        return f"{self.product.name} - {self.name}"


class ProductVariantImage(models.Model):
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='variants/')
    alt_text = models.CharField(max_length=150, blank=True)
    is_main = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order']

    def __str__(self):
        return f"{self.variant.name} Image"

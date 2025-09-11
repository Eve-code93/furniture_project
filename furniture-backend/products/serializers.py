# products/serializers.py
from rest_framework import serializers
from .models import Category, Fabric, Product, ProductImage, ProductVariant, ProductVariantImage

# --------------------------
# CATEGORY SERIALIZER
# --------------------------
class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug', 'description', 'parent',
            'is_active', 'sort_order', 'image', 'meta_title', 'meta_description', 'subcategories'
        ]


# --------------------------
# FABRIC SERIALIZER
# --------------------------
class FabricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fabric
        fields = ['id', 'name', 'description', 'sample_image', 'is_active']


# --------------------------
# PRODUCT IMAGE SERIALIZER
# --------------------------
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'is_main', 'sort_order']


# --------------------------
# PRODUCT VARIANT SERIALIZER
# --------------------------
class ProductVariantSerializer(serializers.ModelSerializer):
    fabric = FabricSerializer(read_only=True)

    class Meta:
        model = ProductVariant
        fields = ['id', 'name', 'sku', 'price_override', 'stock_quantity', 'fabric']


# --------------------------
# PRODUCT SERIALIZER
# --------------------------
class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, required=False)
    variants = ProductVariantSerializer(many=True, required=False)
    main_image = serializers.SerializerMethodField(read_only=True)
    variant_count = serializers.SerializerMethodField(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id','name','slug','sku','description','short_description',
            'category','collection','product_type','base_price','sale_price','cost_price',
            'stock_quantity','low_stock_threshold','track_inventory','production_time_days','requires_approval',
            'dimensions_cm','primary_material','color_family','style','is_active','is_featured','is_bestseller',
            'is_new_arrival','show_in_catalog','supports_customization','custom_request_instructions','care_instructions',
            'warranty_months','assembly_required','assembly_time_minutes','instagram_caption','hashtags','meta_title',
            'meta_description','created_at','updated_at','images','variants','main_image','variant_count'
        ]

    # --------------------------
    # Custom Fields
    # --------------------------
    def get_main_image(self, obj):
        main = obj.images.filter(is_main=True).first()
        return main.image.url if main else None

    def get_variant_count(self, obj):
        return obj.variants.count()

    # --------------------------
    # CREATE / UPDATE OVERRIDES
    # --------------------------
    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        variants_data = validated_data.pop('variants', [])
        product = Product.objects.create(**validated_data)
        self._create_related(product, images_data, variants_data)
        return product

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', None)
        variants_data = validated_data.pop('variants', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if images_data is not None:
            instance.images.all().delete()
            self._bulk_create_images(instance, images_data)

        if variants_data is not None:
            instance.variants.all().delete()
            self._bulk_create_variants(instance, variants_data)

        return instance

    # --------------------------
    # Helper Methods
    # --------------------------
    def _create_related(self, product, images_data, variants_data):
        self._bulk_create_images(product, images_data)
        self._bulk_create_variants(product, variants_data)

    def _bulk_create_images(self, product, images_data):
        objs = [ProductImage(product=product, **img) for img in images_data]
        if objs:
            ProductImage.objects.bulk_create(objs)

    def _bulk_create_variants(self, product, variants_data):
        objs = [ProductVariant(product=product, **v) for v in variants_data]
        if objs:
            ProductVariant.objects.bulk_create(objs)

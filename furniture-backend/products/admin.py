from django.contrib import admin
from .models import Category, Product, ProductImage, ProductVariant, Fabric


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'base_price', 'is_active', 'show_in_catalog', 'created_at')
    list_filter = ('category', 'is_active', 'is_featured', 'is_bestseller', 'is_new_arrival')
    search_fields = ('name', 'slug', 'sku')
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline, ProductVariantInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'sort_order')
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Fabric)
class FabricAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')

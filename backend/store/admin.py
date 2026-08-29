from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Cart, CartItem, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'is_active', 'image_preview']
    list_filter = ['category', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    fields = ['category', 'name', 'slug', 'description', 'price', 'stock',
              'image', 'image_url', 'image_preview', 'is_active']
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:80px;border-radius:6px;" />', obj.image.url)
        if obj.image_url:
            return format_html('<img src="{}" style="height:80px;border-radius:6px;" />', obj.image_url)
        return "(no image yet)"
    image_preview.short_description = "Preview"


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_items', 'total_price']
    inlines = [CartItemInline]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'payment_method', 'payment_status', 'total_price', 'created_at']
    list_filter = ['status', 'payment_method', 'payment_status']
    inlines = [OrderItemInline]

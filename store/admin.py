from django.contrib import admin
from .models import Category, Artist, Product, ProductImage, Cart, CartItem, Wishlist, Order, OrderItem

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'specialty')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'artist', 'price', 'stock_quantity', 'is_featured', 'is_bestseller', 'is_active')
    list_filter = ('category', 'artist', 'is_featured', 'is_bestseller', 'is_active')
    search_fields = ('title', 'material', 'art_style', 'short_description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProductImageInline]
    actions = ['make_featured', 'make_bestseller', 'activate_products']

    def make_featured(self, request, queryset):
        queryset.update(is_featured=True)
    make_featured.short_description = "Mark selected as Featured"

    def make_bestseller(self, request, queryset):
        queryset.update(is_bestseller=True)
    make_bestseller.short_description = "Mark selected as Bestseller"

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_title', 'price', 'quantity', 'subtotal')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer_name', 'customer_mobile', 'grand_total', 'payment_method', 'order_status', 'created_at')
    list_filter = ('order_status', 'payment_status', 'payment_method', 'created_at')
    search_fields = ('order_number', 'customer_name', 'customer_email', 'customer_mobile')
    inlines = [OrderItemInline]

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Wishlist)

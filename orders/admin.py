from django.contrib import admin
from .models import Order, OrderItem, Address, Payment


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ("id", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("id",)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "line1", "city", "country")
    search_fields = ("full_name", "email", "line1", "city")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("order", "provider", "amount", "status", "created_at")
    list_filter = ("provider", "status")

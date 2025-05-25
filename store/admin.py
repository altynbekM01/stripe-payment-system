from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Item, Currency, Order, CustomUser


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    list_filter = ('code', 'name')
    search_fields = ('code', 'name')


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price')
    list_filter = ('name', 'description', 'price')
    search_fields = ('name', 'description', 'price')


class OrderItemInline(admin.TabularInline):
    model = Order.items.through
    extra = 0
    can_delete = False
    verbose_name = "Item"
    verbose_name_plural = "Items"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'paid')
    inlines = [OrderItemInline]
    readonly_fields = ('created_at', 'paid')
    exclude = ('items',)


class OrderInline(admin.TabularInline):
    model = Order
    extra = 0
    readonly_fields = ('id', 'created_at', 'paid')
    can_delete = False


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'get_order_count')
    inlines = [OrderInline]

    def get_order_count(self, obj):
        return obj.orders.count()
    get_order_count.short_description = "Order Count"

from django.contrib import admin
from django.contrib import admin
from .models import Item, Currency

@admin.register(Currency)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    list_filter = ('code', 'name')
    search_fields = ('code', 'name')

@admin.register(Item)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price')
    list_filter = ('name', 'description', 'price')
    search_fields = ('name', 'description', 'price')




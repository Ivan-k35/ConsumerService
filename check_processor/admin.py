from django.contrib import admin
from .models import Place, Purchase, Item, CategoryAnalytics, TotalAnalytics


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ['place_id', 'place_name']


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'timestamp', 'place_id', 'total_amount', 'payment_method']
    list_filter = ['timestamp', 'place_id', 'payment_method']
    search_fields = ['transaction_id']


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['purchase', 'product_id', 'quantity', 'price', 'category']
    list_filter = ['category']


@admin.register(CategoryAnalytics)
class CategoryAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['place', 'category', 'total_spent', 'average_receipt']
    list_filter = ['place', 'category']


@admin.register(TotalAnalytics)
class TotalAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['place', 'total_purchases', 'average_receipt', 'total_nds', 'total_tips']
    list_filter = ['place']

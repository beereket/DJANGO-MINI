from django.contrib import admin
from .models import TradeOffer

@admin.register(TradeOffer)
class TradeOfferAdmin(admin.ModelAdmin):
    list_display = ('id', 'seller', 'product', 'price', 'created_at')
    list_filter = ('seller',)
    search_fields = ('seller__username', 'product__name')
    ordering = ('id',)

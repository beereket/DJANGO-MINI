from rest_framework import serializers
from .models import TradeOffer

class TradeOfferSerializer(serializers.ModelSerializer):
    seller = serializers.HiddenField(default=serializers.CurrentUserDefault())  # 👈 seller устанавливается автоматически

    class Meta:
        model = TradeOffer
        fields = ['id', 'product', 'price', 'created_at', 'seller']

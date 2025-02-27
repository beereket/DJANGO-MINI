from rest_framework import serializers
from .models import Payment, OrderHistory


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class OrderHistorySerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source="product.name")

    class Meta:
        model = OrderHistory
        fields = ['id', 'buyer', 'product_name', 'quantity', 'total_price', 'created_at']
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from notifications.models import Notification
from users.models import User
from .models import Payment
from cart.models import CartItem
from trading.models import TradeOffer
from sales.models import OrderHistory
from rest_framework import generics
from .serializers import OrderHistorySerializer
from django.http import FileResponse
from .utils import generate_invoice

class PayCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if request.user.role != "buyer":
            return Response({"error": "Only buyers can make payments."}, status=403)

        cart_items = CartItem.objects.filter(user=request.user)
        if not cart_items.exists():
            return Response({"error": "Cart is empty"}, status=400)

        total_price = sum(
            item.product.price * item.quantity if item.product else item.trade_offer.price
            for item in cart_items
        )

        # Create a payment record
        payment = Payment.objects.create(user=request.user, amount=total_price, payment_status=True)

        Notification.objects.create(
            user=request.user,
            message="🎉 Congratulations! Your order has been placed successfully!"
        )

        trade_sellers = {item.trade_offer.seller for item in cart_items if item.trade_offer}
        for seller in trade_sellers:
            Notification.objects.create(
                user=seller,
                message="📢 Your trade offer has been sold!"
            )

        if any(item.product for item in cart_items):
            admin_users = User.objects.filter(role__iexact="admin")
            for admin in admin_users:
                Notification.objects.create(
                    user=admin,
                    message="⚠ New products have been sold!"
                )

        for item in cart_items:
            if item.product:  # Учитываем только `products`, а не `trading`
                OrderHistory.objects.create(
                    buyer=request.user,
                    product=item.product,
                    quantity=item.quantity,
                    total_price=item.product.price * item.quantity
                )

        # Remove items from cart after payment
        cart_items.delete()

        return Response({"message": "Payment successful!", "payment_id": payment.id}, status=201)

class OrderHistoryView(generics.ListAPIView):
    serializer_class = OrderHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return OrderHistory.objects.filter(buyer=self.request.user)

class InvoicePDFView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, order_id):
        try:
            order = OrderHistory.objects.get(id=order_id, buyer=request.user)
        except OrderHistory.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)

        pdf_buffer = generate_invoice(order.id)
        return FileResponse(pdf_buffer, as_attachment=True, filename=f"Invoice_{order.id}.pdf")

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CartItem
from .serializers import CartItemSerializer

class CartListView(generics.ListAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

class RemoveFromCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, item_id):
        try:
            cart_item = CartItem.objects.get(id=item_id, user=request.user)
            cart_item.delete()
            return Response({"message": "Item removed from cart!"}, status=200)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found"}, status=404)

from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import TradeOffer
from .serializers import TradeOfferSerializer
from cart.models import CartItem


# View all trade offers
class TradeOfferListView(generics.ListAPIView):
    queryset = TradeOffer.objects.all()
    serializer_class = TradeOfferSerializer
    permission_classes = [permissions.AllowAny]


# Create a trade offer (Only buyers can sell items)
class TradeOfferCreateView(generics.CreateAPIView):
    serializer_class = TradeOfferSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role not in ["buyer"]:
            raise PermissionDenied("Only buyers can create trade offers.")

        serializer.save(seller=self.request.user)

class AddTradeToCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, offer_id):
        if request.user.role != "buyer":
            return Response({"error": "Only buyers can purchase trade offers."}, status=403)
        try:
            offer = TradeOffer.objects.get(id=offer_id)
        except TradeOffer.DoesNotExist:
            return Response({"error": "Trade offer not found"}, status=404)

        if offer.seller == request.user:
            return Response({"error": "You cannot buy your own item."}, status=400)

        CartItem.objects.create(user=request.user, trade_offer=offer)

        return Response({"message": "Trade offer added to cart!"}, status=201)

from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import RegisterSerializer, UserSerializer
from cart.models import CartItem
from cart.serializers import CartItemSerializer  # 👈 Новый импорт
from drf_yasg import openapi
from rest_framework.serializers import Serializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = Serializer  # 👈 Добавляем пустой сериализатор

    @swagger_auto_schema(
        operation_description="Logout user by blacklisting the refresh token",
        responses={200: openapi.Response("Successfully logged out")}
    )
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out."}, status=200)
        except Exception as e:
            return Response({"error": "Invalid token"}, status=400)

# Получить список продаж (продавец видит товары, которые у него купили)
class UserSalesView(generics.ListAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(product__seller=self.request.user)

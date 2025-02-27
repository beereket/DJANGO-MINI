from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from rest_framework.exceptions import PermissionDenied
from cart.models import CartItem
from django.shortcuts import render

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

class ProductCreateView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role == 'seller':
            serializer.save(seller=self.request.user)
        else:
            raise PermissionDenied("Only sellers can add products.")

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

class ProductUpdateView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Update product (only PUT allowed)",
        request_body=ProductSerializer,
        responses={200: ProductSerializer()}
    )
    def put(self, request, *args, **kwargs):
        if self.request.user.role == 'seller':
            return super().put(request, *args, **kwargs)
        else:
            raise PermissionDenied("Only sellers can edit products.")

class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Delete product",
        responses={204: "Product deleted successfully"}
    )
    def delete(self, request, *args, **kwargs):
        if self.request.user.role == 'seller':
            return super().delete(request, *args, **kwargs)
        else:
            raise PermissionDenied("Only sellers can delete products.")

class AddProductToCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, product_id):
        if request.user.role != "buyer":
            return Response({"error": "Only buyers can add products to cart."}, status=403)
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)

        CartItem.objects.create(user=request.user, product=product, quantity=1)
        return Response({"message": "Product added to cart!"}, status=201)

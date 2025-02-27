from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from sales.models import OrderHistory
from users.models import User
from products.models import Product
from django.db.models import Count, Sum

class SalesAnalyticsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        # ✅ Считаем количество заказов по `OrderHistory`
        total_sales = OrderHistory.objects.count()
        total_revenue = OrderHistory.objects.aggregate(Sum("total_price"))["total_price__sum"]

        return Response({
            "total_sales": total_sales,
            "total_revenue": total_revenue if total_revenue else 0
        })

class UserAnalyticsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        active_users = User.objects.filter(is_active=True).count()
        total_users = User.objects.count()
        return Response({"total_users": total_users, "active_users": active_users})

class ProductAnalyticsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        # ✅ Самые популярные товары (по `OrderHistory`)
        popular_products = Product.objects.annotate(order_count=Count("sold_products")).order_by("-order_count")[:5]
        data = [{"product": p.name, "orders": p.order_count} for p in popular_products]

        return Response({"popular_products": data})

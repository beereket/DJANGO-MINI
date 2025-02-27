from django.urls import path
from .views import SalesAnalyticsView, UserAnalyticsView, ProductAnalyticsView

urlpatterns = [
    path('sales/', SalesAnalyticsView.as_view(), name='analytics-sales'),
    path('users/', UserAnalyticsView.as_view(), name='analytics-users'),
    path('products/', ProductAnalyticsView.as_view(), name='analytics-products'),
]

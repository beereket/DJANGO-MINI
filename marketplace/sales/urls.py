from django.urls import path
from .views import PayCartView, OrderHistoryView, InvoicePDFView

urlpatterns = [
    path('pay/', PayCartView.as_view(), name='cart-pay'),
    path('history/', OrderHistoryView.as_view(), name='order-history'),
    path('invoice/<int:order_id>/', InvoicePDFView.as_view(), name='order-invoice'),
]

from django.urls import path
from .views import CartListView, RemoveFromCartView

urlpatterns = [
    path('', CartListView.as_view(), name='cart-list'),
    path('remove/<int:item_id>/', RemoveFromCartView.as_view(), name='cart-remove'),
]
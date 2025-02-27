from django.urls import path
from .views import TradeOfferListView, TradeOfferCreateView, AddTradeToCartView

urlpatterns = [
    path('offers/', TradeOfferListView.as_view(), name='trade-offers'),
    path('offers/add/', TradeOfferCreateView.as_view(), name='trade-offer-add'),
    path('offers/<int:offer_id>/add_to_cart/', AddTradeToCartView.as_view(), name='trade-add-to-cart'),
]
from django.urls import path
from .views import ProductListView, ProductCreateView, ProductDetailView, AddProductToCartView, ProductDeleteView, ProductUpdateView

urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('add/', ProductCreateView.as_view(), name='product-create'),
    path('<int:pk>/edit/', ProductUpdateView.as_view(), name='product-update'),
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('<int:product_id>/add_to_cart/', AddProductToCartView.as_view(), name='product-add-to-cart'),
]

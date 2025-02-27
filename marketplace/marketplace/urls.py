from django.contrib import admin
from django.urls import path, include
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls.static import static
from django.conf import settings
from products.views import home

# Настройки Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Marketplace API",
        default_version='v1',
        description="API для продажи и торговли",
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path('', home, name='home'),

    path('admin/', admin.site.urls),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/users/', include('users.urls')),
    path('api/products/', include('products.urls')),
    path('api/trading/', include('trading.urls')),
    path('api/sales/', include('sales.urls')),
    path('api/analytics/', include('analytics.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/cart/', include('cart.urls')),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# ✅ Разрешаем Django раздавать media-файлы (ТОЛЬКО В `DEBUG=True`!)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
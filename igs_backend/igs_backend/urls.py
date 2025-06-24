

from django.conf import settings
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="KEDESH API",
        default_version='v2',
        description="Description of the API endpoints",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="mcharoprofg23@gmail.com"),
        license=openapi.License(name="MIT"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', lambda request: redirect('/admin/')),
    path("admin/", admin.site.urls),
    path('api/v2/payment/', include('payment.urls')),
    path('api/v2/user/', include('user.urls')),
    path('api/v2/auth/', include('authentication.urls')),
    path('api/v2/location/', include('location.urls')),
    path('api/v2/house/', include('house.urls')),
    path('api/v2/booking/', include('booking.urls')),
    path('api/v2/account/', include('account.urls')),
    path('api/v2/property/', include('property.urls')),
    path('api/v2/room/', include('room.urls')),
    path('api/v2/company_information/', include('settings.urls')),
    path('api/v2/land/', include('land.urls')),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "KEDESH Administration Dashboard"
admin.site.site_title = "KEDESH"
admin.site.index_title = "KEDESH"
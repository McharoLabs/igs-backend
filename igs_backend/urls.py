"""
URL configuration for igs_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

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
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path("admin/", admin.site.urls),
    # path('api/v2/payment/', include('payment.urls')),
    path('api/v2/user/', include('user.urls')),
    path('api/v2/auth/', include('authentication.urls')),
    path('api/v2/location/', include('location.urls')),
    path('api/v2/house/', include('house.urls')),
    path('api/v2/booking/', include('booking.urls')),
    path('api/v2/account/', include('account.urls')),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "KEDESH Administration Dashboard"
admin.site.site_title = "KEDESH"
admin.site.index_title = "KEDESH"
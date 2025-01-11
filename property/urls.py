from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r'properties', views.PropertyImageViewSet, basename='property')
urlpatterns = router.urls

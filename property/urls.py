from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r'properties', views.PropertyImageViewSet, basename='property')
router.register(r'properties', views.PropertyViewSet, basename='property_status')
urlpatterns = router.urls

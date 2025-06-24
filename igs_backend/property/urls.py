from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r'images', views.PropertyImageViewSet, basename='image')
router.register(r'properties', views.PropertyViewSet, basename='property')
urlpatterns = router.urls

from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r'land-images', views.LandImagesViewSet, basename='image')
router.register(r'lands', views.LandViewSet, basename='land')
urlpatterns = router.urls

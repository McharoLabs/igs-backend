from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r'districts', views.DistrictViewSet, basename='district')
router.register(r'regions', views.RegionViewSet, basename='region')
urlpatterns = router.urls
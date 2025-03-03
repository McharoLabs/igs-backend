from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r'districts', views.DistrictViewSet, basename='district')
router.register(r'regions', views.RegionViewSet, basename='region')
router.register(r'wards', views.WardViewSet, basename='ward')
router.register(r'streets', views.StreetViewSet, basename='street')

urlpatterns = router.urls
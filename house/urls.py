from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r'houses', views.HouseViewSet, basename='house')
router.register(r'rooms', views.RoomViewSet, basename='room')
router.register(r'images', views.PropertyImageViewSet, basename='image')
urlpatterns = router.urls

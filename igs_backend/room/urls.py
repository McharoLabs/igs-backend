from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r'rooms', views.RoomViewSet, basename='room')
urlpatterns = router.urls

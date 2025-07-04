from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r'bookings', views.BookingViewSet, basename='booking')
urlpatterns = router.urls

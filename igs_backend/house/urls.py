from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r'houses', views.HouseViewSet, basename='house')
urlpatterns = router.urls

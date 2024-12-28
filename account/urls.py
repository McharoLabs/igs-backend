from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r'accounts', views.AccountViewSet, basename='account')
urlpatterns = router.urls

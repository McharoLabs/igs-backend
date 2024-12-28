from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r'accounts', views.AccountViewSet, basename='account')
router.register(r'plans', views.SubscriptionPlanViewSet, basename='plan')
urlpatterns = router.urls

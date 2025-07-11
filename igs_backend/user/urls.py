from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AgentViewSet, UserViewSet

router = DefaultRouter()

router.register(r'agents', AgentViewSet, basename='agent')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = router.urls

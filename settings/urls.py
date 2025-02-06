
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r'informations', views.CompanyInformation, basename='company_information')
urlpatterns = router.urls

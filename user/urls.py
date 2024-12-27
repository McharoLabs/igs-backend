from django.urls import path
from . import views

urlpatterns = [
    path('agent/register', views.AgentRegistrationView.as_view(), name='agent-registration'),
    path('land-lord/register', views.LandLordRegistrationView.as_view(), name='land-lord-registration'),
]

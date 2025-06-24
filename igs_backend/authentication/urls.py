from django.urls import path
from . import views

urlpatterns = [
    path('sign-in', views.SignInAPIView.as_view(), name='sign_in'),
    path('sign-out', views.SignOutAPIView.as_view(), name='sign_out'),
]

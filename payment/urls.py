from django.urls import path
from . import views

urlpatterns = [
    path('payment-webhook/', views.PaymentWebHook.as_view()),
]
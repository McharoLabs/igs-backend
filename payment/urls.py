from django.urls import path
from .views import PaymentView

urlpatterns = [
    path('all', PaymentView.as_view(), name='payment-list-create'),
]

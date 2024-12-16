from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from rest_framework.pagination import PageNumberPagination

from .models import Payment
from .serializers import PaymentResponseSerializer, PaymentRequestSerializer

@method_decorator(never_cache, name='dispatch')
class PaymentView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny] 

    @swagger_auto_schema(
        operation_description="Get a list of payments",
        responses={200: PaymentResponseSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        payments = Payment.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(payments, request)
        serializer = PaymentResponseSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new payment",
        request_body=PaymentRequestSerializer,
        responses={201: PaymentResponseSerializer},
    )
    def post(self, request, *args, **kwargs):
        request_serializer = PaymentRequestSerializer(data=request.data)
        if request_serializer.is_valid():
            payment = request_serializer.save()
            response_serializer = PaymentResponseSerializer(payment)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

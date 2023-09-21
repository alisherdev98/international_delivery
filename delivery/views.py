from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView, CreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django_filters.rest_framework import DjangoFilterBackend

from delivery.models import Delivery, DeliveryType
from delivery.serializers import (
    DeliveryTypeModelSerializer,
    DeliveryModelSerializer,
    TransportDeliverySerializer,
    DeliveryCreatingQueryParamSerializer
)
from delivery.tasks import ProducerMQ
from delivery.actions import TransportDeliveryLinker
from delivery.repositories import DeliveryRepository
from delivery.filters import DeliveryPagination

#  TODO When session is update?
class DeliveryTypeView(ListAPIView):
    queryset = DeliveryType.objects.all()
    serializer_class = DeliveryTypeModelSerializer


class SessionQuerysetMixin:
    def get_queryset(self):
        queryset = super().get_queryset()

        session_key = self.request.session.session_key

        return queryset.filter(
            session_key=session_key
        )


class DeliveryView(SessionQuerysetMixin, ListCreateAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliveryModelSerializer
    pagination_class = DeliveryPagination

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='message_broker',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description='Creating by celery worker(0) or rabbitmq queue(1)',
                enum=[0, 1],
                required=False,
            ),
        ]
    )
    def post(self, request, *args, **kwargs):
        if not request.session.session_key:
            request.session.create()

        request.data['session_key'] = request.session.session_key

        query_serializer = DeliveryCreatingQueryParamSerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        message_broker = query_serializer.validated_data.get('message_broker')

        if message_broker:
            return self.publish_mq(request_data=request.data)
        else:
            return super().post(request, *args, **kwargs)
        
    def publish_mq(self, request_data):
        serializer = self.serializer_class(data=request_data)
        serializer.is_valid(raise_exception=True)
        # validated_data = serializer.validated_data
        
        ProducerMQ().publish(request_data)  # TODO how add id to delivery
        return Response(
            data={'success': True},
            status=status.HTTP_201_CREATED,
        )


class DeliveryRetrieveView(SessionQuerysetMixin, RetrieveAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliveryModelSerializer


# class TransportDeliveryView(APIView):
class TransportDeliveryView(SessionQuerysetMixin, GenericAPIView):
    request_serializer_class = TransportDeliverySerializer
    queryset = Delivery.objects.all()

    @swagger_auto_schema(
        operation_id='Привязка транспортной компании к доставке',
        tags=['transport company'],
        request_body=request_serializer_class,
        responses={
            200: openapi.Response(
                description='Success',
                examples={
                    "application/json": {
                        "success": True,
                    }
                }
            ),
            400: openapi.Response(
                description='Fail',
                examples={
                    "application/json": {
                        "success": False,
                    }
                },
            ),
            400: openapi.Response(
                description='Locked',
                examples={
                    "application/json": {
                        "success": 'locked',
                    }
                },
            ),
        },
    )
    def post(self, request, pk):
        # get_object_or_404(
        #     Delivery,
        #     pk=pk,
        #     session_key_id=self.request.session.session_key,  # TODO remove number one
        # )
        self.get_object()
        
        serializer = self.request_serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        company_id = serializer.validated_data['company_id']
        
        result = TransportDeliveryLinker(
            delivery_id=pk,
            company_id=company_id,
            repository=DeliveryRepository(),
        ).run()
        
        if result is True:
            status_code = status.HTTP_200_OK
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            
        return Response(
            data={'status': result},
            status=status_code,
        )

        
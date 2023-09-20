from django.shortcuts import render
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status

from delivery.models import Delivery, DeliveryType
from delivery.serializers import DeliveryTypeModelSerializer, DeliveryModelSerializer
from delivery.tasks import ProducerMQ

#  TODO When session is update?
class DeliveryTypeView(ListAPIView):
    queryset = DeliveryType.objects.all()
    serializer_class = DeliveryTypeModelSerializer


class DeliveryView(ListCreateAPIView, RetrieveAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliveryModelSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        session_key = self.request.session.session_key

        return queryset.filter(
            session_key=session_key
        )
    
    def get(self, request, *args, **kwargs):
        if kwargs.get('pk'):
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not request.session.session_key:
            request.session.create()

        request.data['session_key'] = request.session.session_key

        if request.query_params.get('message_broker'):
            return self.publish_mq(request_data=request.data)
        else:
            return super().post(request, *args, **kwargs)
        
    def publish_mq(self, request_data):
        serializer = self.serializer_class(data=request_data)
        serializer.is_valid(raise_exception=True)
        # validated_data = serializer.validated_data
        
        publishing = ProducerMQ().publish(request_data)  # TODO how add id to delivery
        return Response(
            data={'success': True},
            status=status.HTTP_201_CREATED,
        )


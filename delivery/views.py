from django.shortcuts import render
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView

from delivery.models import Delivery, DeliveryType
from delivery.serializers import DeliveryTypeModelSerializer, DeliveryModelSerializer


class DeliveryTypeView(ListAPIView):
    queryset = DeliveryType.objects.all()
    serializer_class = DeliveryTypeModelSerializer


class DeliveryView(ListCreateAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliveryModelSerializer

    def post(self, request, *args, **kwargs):
        if not request.session.session_key:
            request.sesion.create()
        
        return super().post(request, *args, **kwargs)


class DeliveryRetrieveView(RetrieveAPIView):  # TODO add retrive in DeliveryView
    queryset = Delivery.objects.all()
    serializer_class = DeliveryModelSerializer
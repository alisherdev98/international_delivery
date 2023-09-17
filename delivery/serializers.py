from rest_framework import serializers

from delivery.models import Delivery, DeliveryType


class DeliveryTypeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryType
        fields = '__all__'


class DeliveryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = '__all__'

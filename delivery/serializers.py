from rest_framework import serializers
from delivery.enums import DeliveryCreatingTypeEnum

from delivery.models import Delivery, DeliveryType


class DeliveryTypeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryType
        fields = '__all__'


class DeliveryModelSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)

        if not data['delivery_cost']:
            data['delivery_cost'] = 'Не расcчитано'
        return data
    
    class Meta:
        model = Delivery
        fields = '__all__'
        extra_kwargs = {
            'session_key': {
                'write_only': True
            }
        }


class TransportDeliverySerializer(serializers.Serializer):
    company_id = serializers.IntegerField()


class DeliveryCreatingQueryParamSerializer(serializers.Serializer):
    DELIVERY_CREATING_CHOICES = [
        (
            type_enum.value,
            type_enum.name.lower()
        ) for type_enum in DeliveryCreatingTypeEnum
    ]

    message_broker = serializers.ChoiceField(choices=DELIVERY_CREATING_CHOICES, required=False)

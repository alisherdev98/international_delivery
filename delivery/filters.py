import django_filters

from delivery.enums import DeliveryCreatingTypeEnum
from rest_framework.pagination import PageNumberPagination


# class DeliveryCreateTypeFilterSet(django_filters.FilterSet):
#     message_broker = django_filters.ChoiceFilter(choices=DELIVERY_CREATING_CHOICES)


class DeliveryPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page[size]'
    page_query_param = 'page[number]'
from django.contrib import admin

from delivery.models import Delivery, DeliveryType

admin.site.register(Delivery)
admin.site.register(DeliveryType)
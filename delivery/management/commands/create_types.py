from typing import Any
from django.core.management import BaseCommand

from delivery.repositories import DeliveryTypeRepository
from delivery.enums import DeliveryTypeEnum


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        objects_data = [{
            'id': delivery_type_enum.id,
            'name': delivery_type_enum.name.lower(),
            'full_name': delivery_type_enum.full_name,
        } for delivery_type_enum in DeliveryTypeEnum]

        delivery_type_objects = DeliveryTypeRepository().bulk_create(objects_data)

        self.stdout.write(self.style.SUCCESS(f"Delivery type with quantity {len(delivery_type_objects)} created: {delivery_type_objects}"))

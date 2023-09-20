from typing import Any
from django.core.management import BaseCommand

from delivery.tasks import process_delivery_delivery_cost


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        updated_delivery_quantity = process_delivery_delivery_cost()
        # self.stdout.write(self.style.SUCCESS('The task of processing delivery cost is running!'))
        self.stdout.write(self.style.SUCCESS("The task of processing delivery cost "
                                                f"is updated {updated_delivery_quantity} delivery!"))
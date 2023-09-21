from delivery.repositories import DeliveryRepository


class TransportDeliveryLinker:
    def __init__(self, delivery_id, company_id, repository: DeliveryRepository) -> None:
        self.delivery_id = delivery_id
        self.company_id = company_id
        self.repository = repository

    def run(self):
        return self.repository.select_one_for_update(
            update_fields={
                'company_id': self.company_id,
            },
            pk=self.delivery_id,
            company_id__isnull=True,
        )
        
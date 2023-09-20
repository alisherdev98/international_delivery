import abc
from django.db.models import Model

from delivery.models import DeliveryType, Delivery

    
class AbstractRepository(abc.ABC):
    @abc.abstractproperty
    def model(self) -> Model:
        ...

    def read(self, **filter_kwargs):
        return self.model.objects.get(**filter_kwargs)
    
    def list(self, **filter_kwargs):
        return list(self.model.objects.filter(**filter_kwargs))


    def bulk_create(self, datas_sequence):
        instances = []
        
        for object_data in datas_sequence:
            instances.append(
                self.model(**object_data)
            )

        return self.model.objects.bulk_create(
            instances,
            # update_conflicts=True,
            # update_fields=('name', 'full_name',),
            # unique_fields=('id',),
            ignore_conflicts=True,
        )
    
    def bulk_update(self, objects_sequence, update_fields):
        updated_count = self.model.objects.bulk_update(
            objects_sequence,
            update_fields,
        )
        return set(objects_sequence)
        
class DeliveryTypeRepository(AbstractRepository):
    model = DeliveryType


class DeliveryRepository(AbstractRepository):
    model = Delivery

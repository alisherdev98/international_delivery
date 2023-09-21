import abc
from django.db.models import Model
from django.db import transaction
from time import time
from time import sleep
from django.db.utils import OperationalError

from delivery.models import DeliveryType, Delivery

    
class AbstractRepository(abc.ABC):
    @abc.abstractproperty
    def model(self) -> Model:
        ...

    def create(self, data):
        return self.model.objects.create(**data)

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
    
    def select_one_for_update(self, update_fields: dict, **filter_kwargs):
        assert update_fields
        
        with transaction.atomic():
            try:
                object = self.model.objects.select_for_update(nowait=True).get(**filter_kwargs)
            except self.model.DoesNotExist:
                return False
            except OperationalError:
                return 'locked'
            
            for name, value in update_fields.items():
                setattr(object, name, value)

            object.save()
            
            return True

        
        
class DeliveryTypeRepository(AbstractRepository):
    model = DeliveryType


class DeliveryRepository(AbstractRepository):
    model = Delivery

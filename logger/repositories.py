import abc

from international_delivery.connections import MongoDBConnection


class AbstractMongoRepository(abc.ABC):
    @abc.abstractproperty
    def collection(self):
        ...

    def create(self, data):
        return self.collection.insert_one(data).inserted_id

    def bulk_create(self, data_sequence: list):
        return self.collection.insert_many({"arr": data_sequence})

    def read(self, **filter_kwargs):
        return self.collection.findOne(filter_kwargs)
    
    def list(self, **filter_kwargs):
        return list(self.collection.find(filter_kwargs))

    
class DeliveryLogRepository(AbstractMongoRepository):
    collection = MongoDBConnection().get_collection('delivery_log')

import abc
from celery import shared_task

from delivery.repositories import DeliveryRepository
from delivery.requesters import CBRDailyRequester
from django.core.cache import cache


# celery
@shared_task(name='process_delivery_ruble_cost')
def process_delivery_ruble_cost():
    delivery_repository = DeliveryRepository()
    
    unprocessing_delivery = delivery_repository.list(
        ruble_cost__isnull=True
    )
    requester = CBRDailyRequester()

    exchange_rate = CBRDailyRequestExchanger(requester).get_rate()

    for delivery in unprocessing_delivery:
        delivery_cost = DeliveryCalculator(
            weight=delivery.weight,
            content_cost=delivery.content_cost,
            exchange_rate=exchange_rate,
        ).calculate()
        delivery.ruble_cost = delivery_cost

    updated_delivery_quantity = delivery_repository.bulk_update(
        objects_sequence=unprocessing_delivery,
        update_fields=['ruble_cost'],
    )
    return updated_delivery_quantity


# app tasks
class DeliveryCalculator:
    def __init__(self, weight, content_cost, exchange_rate) -> None:
        self.weight = weight
        self.content_cost = content_cost
        # self.exchanger = exchanger
        self.exchange_rate = exchange_rate

    def calculate(self):
        # exchange_rate = self.get_exchange_rate()

        dollar_delivery_cost = (self.weight * 0.5 + self.content_cost * 0.01)
        delivery_cost = dollar_delivery_cost * self.exchange_rate
        
        return delivery_cost


    # def get_exchange_rate(self):
    #     return self.exchanger.get_rate()
    

# exchanger
class AbstractExchanger(abc.ABC):
    """
        Template method abstract class
    """
    @abc.abstractmethod
    def get_rate():
        ...

    
class CBRDailyRequestExchanger(AbstractExchanger):
    def __init__(self, requester: CBRDailyRequester) -> None:
        self.requester = requester

    def get_rate(self):
        cbr_daily_json = self.requester.get_exchange()
        usd_valute = cbr_daily_json['Valute']['USD']['Value']
        return usd_valute


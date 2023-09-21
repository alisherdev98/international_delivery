import abc
import json
from datetime import timedelta
from functools import reduce
import logging
from celery import shared_task
from django.core.cache import cache
from django.utils import timezone

from international_delivery.connections import RabbitMQConnection
from delivery.repositories import DeliveryRepository
from delivery.requesters import CBRDailyRequester
from delivery.enums import DeliveryTypeEnum
from delivery.serializers import DeliveryModelSerializer
from logger.tasks import delivery_logger
from logger.repositories import DeliveryLogRepository


# celery
@shared_task(name='process_delivery_delivery_cost')
@delivery_logger
def process_delivery_delivery_cost():
    delivery_repository = DeliveryRepository()
    
    unprocessing_delivery = delivery_repository.list(
        delivery_cost__isnull=True
    )
    requester = CBRDailyRequester()

    exchange_rate = CBRDailyRequestExchanger(requester).get_rate()

    for delivery in unprocessing_delivery:
        delivery_cost = DeliveryCalculator(
            weight=delivery.weight,
            content_cost=delivery.content_cost,
            exchange_rate=exchange_rate,
        ).calculate()
        delivery.delivery_cost = delivery_cost
        # delivery.updated_at = timezone.localtime()

    updated_delivery_objects = delivery_repository.bulk_update(
        objects_sequence=unprocessing_delivery,
        update_fields=['delivery_cost'],
    )
    return updated_delivery_objects


@shared_task(name='calculate_daily_delivery_cost')
def calculate_daily_delivery_cost():
    # yesterday = timezone.localtime() - timedelta(days=1)
    yesterday = timezone.localtime()
    start_date = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = start_date + timedelta(days=1) - timedelta(seconds=1)
    
    result = {}

    for delivery_type_enum in DeliveryTypeEnum:
        delivery_type = delivery_type_enum.name.lower()

        delivery_data = DeliveryLogRepository().list(
            type=delivery_type,
            updated_at={
                '$gte': start_date,
                '$lt': end_date,
            },
        )
        if delivery_data:
            type_delivery_cost = reduce(
                # lambda x, y: x['delivery_cost'] + y['delivery_cost'],
                reduce_func,
                delivery_data,
                0,
            )
        else:
            type_delivery_cost = 0

        result[delivery_type] = type_delivery_cost

    return result


def reduce_func(x, y):
    if not isinstance(x, (int, float)):
        x = x['delivery_cost']

    if not isinstance(y, (int, float)):
        y = y['delivery_cost']

    return x + y


# app tasks
class DeliveryCalculator:
    def __init__(self, weight, content_cost, exchange_rate) -> None:
        self.weight = weight
        self.content_cost = content_cost
        # self.exchanger = exchanger
        self.exchange_rate = exchange_rate

    def calculate(self):
        dollar_delivery_cost = (self.weight * 0.5 + self.content_cost * 0.01)
        delivery_cost = dollar_delivery_cost * self.exchange_rate
        
        return round(delivery_cost, 2)


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


# rabbitmq
class ProducerMQ:
    def publish(self, body):
        connection = RabbitMQConnection()
        channel = connection.get_channel()
        queue_name = connection.queue_name  # TODO add descriptor

        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=json.dumps(body),
        )


class ConsumerMQ:
    def consume(self, callback_func):
        connection = RabbitMQConnection()
        self.channel = connection.get_channel()
        queue_name = connection.queue_name  # TODO add descriptor

        self.channel.basic_consume(
            queue=queue_name,
            on_message_callback=callback_func,
            auto_ack=True,
        )
    
    def start_consuming(self):
        print('READY')
        self.channel.start_consuming()

    def stop_consuming(self):
        self.channel.stop_consuming()

def callback_mq(ch, method, properties, body):
    data = json.loads(body)

    requester = CBRDailyRequester()

    exchange_rate = CBRDailyRequestExchanger(requester).get_rate()

    delivery_cost = DeliveryCalculator(
        weight=data['weight'],
        content_cost=data['content_cost'],
        exchange_rate=exchange_rate,
    ).calculate()
    data['delivery_cost'] = delivery_cost

    serializer = DeliveryModelSerializer(data=data)
    serializer.is_valid()
    object = serializer.save()
    print(object)




    

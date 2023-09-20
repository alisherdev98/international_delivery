import json
import logging
from functools import wraps
from typing import Set
from pymongo import MongoClient

from delivery.models import Delivery

http_logger = logging.getLogger('outer_request')
delivery_cost_logger = logging.getLogger('delivery_cost')


def request_logger(api_method):
    
    @wraps(api_method)
    def _wrapper(*args, **kwargs):
        response = api_method(*args, **kwargs)


        request_instance = args[0]

        url = request_instance.domain + kwargs['path']

        log_extra_data = {
            'request_url': url,
            'request_headers': json.dumps(
                request_instance.headers,
                indent=4,
            ),
            'request_body': kwargs.get('body'),
            'response_status_code': response.status_code,
            'response_headers': json.dumps(
                dict(response.headers),
                indent=4,
            ),
            'response_body': json.dumps(
                response.json(),
                indent=4
            ),
        }
        
        http_logger.info(
            msg='api request log',
            extra={
                'log_extra_data': log_extra_data
            },
        )

        return response

    return _wrapper


def delivery_logger(func):
    def wrapper(*args, **kwargs):
        result: Set[Delivery] = func(*args, **kwargs)

        for delivery_object in result:
            delivery_cost_logger.info(
                msg='delivery cost log',
                extra={'log_extra_data': {
                    'delivery_id': delivery_object.id,
                    'type': delivery_object.type.name,  # TODO name or type_id
                    'delivery_cost': delivery_object.delivery_cost,
                    'updated_at': delivery_object.updated_at,
                }}
            )

    return wrapper

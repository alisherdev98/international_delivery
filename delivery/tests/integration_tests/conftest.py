import pytest
from datetime import datetime
from rest_framework.test import APIClient
from django.core.management import call_command
from django.contrib.sessions.models import Session

from delivery.tasks import ProducerMQ
from delivery.repositories import DeliveryRepository
from delivery.views import SessionQuerysetMixin


@pytest.fixture
def delivery_data():
    return {
        "name": "testing",
        "weight": 4,
        "type": 1,
        "content_cost": 1000,
    }


@pytest.fixture
def session_object():
    return Session.objects.create(
        session_key='8nb23ussom0mq9lh5e7xats59l77f1ex',
        session_data='session_data_test',
        expire_date=datetime.now(),
    )


@pytest.fixture(scope='module')
def api_client():
    return APIClient()


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('create_types')


@pytest.fixture
def mock_rabbitmq_publisher(monkeypatch):
    def mock_publish(self_object, data):
        return True

    monkeypatch.setattr(ProducerMQ, 'publish', value=mock_publish)


@pytest.fixture
def delivery_object(delivery_data, session_object):
    return DeliveryRepository().create({
        'session_key_id': session_object.session_key,
        'type_id': delivery_data.pop('type'),
        **delivery_data,
    })


@pytest.fixture
def mock_get_queryset(delivery_object, monkeypatch):
    def mock_get_queryset(self_object):
        queryset = super(SessionQuerysetMixin, self_object).get_queryset()

        return queryset.filter(
            session_key=delivery_object.session_key_id,
        )
    
    monkeypatch.setattr(SessionQuerysetMixin, 'get_queryset', value=mock_get_queryset)
    return delivery_object



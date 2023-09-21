import json
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from delivery.enums import DeliveryTypeEnum
from http.cookies import SimpleCookie

from delivery.tasks import ProducerMQ


@pytest.mark.django_db
def test_list_delivery_type(api_client):
    url = reverse('delivery_type')

    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.json()) == len(DeliveryTypeEnum)


@pytest.mark.django_db
@pytest.mark.parametrize(
    'query_string', [
        (''),
        ('?message_broker=0'),
        ('?message_broker=1'),
    ]
)
def test_delivery_create(mock_rabbitmq_publisher, api_client: APIClient, delivery_data, query_string):
    url = reverse('delivery') + query_string

    response = api_client.post(
        path=url,
        data=json.dumps(delivery_data),
        content_type='application/json',
        # **{'QUERY_STRING': query_string},
    )

    assert response.status_code == 201


@pytest.mark.django_db
def test_delivery_list(api_client, mock_get_queryset):  # TODO check session_key
    url = reverse('delivery')

    # api_client.session._SessionBase__session_key = delivery_object.session_key_id
    # api_client = APIClient(SESSION_ID=delivery_object.session_key_id)
    
    # api_client.cookies = SimpleCookie({'sessionid': delivery_object.session_key_id})


    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.json()['results']) > 0


@pytest.mark.django_db
def test_delivery_retrieve(api_client, mock_get_queryset):
    url = reverse('delivery_retrieve', kwargs={'pk': mock_get_queryset.id})

    response = api_client.get(url)

    assert response.status_code == 200
    assert response.json()['delivery_cost'] == 'Не расcчитано'

    
@pytest.mark.django_db
def test_link_transport_company(api_client, mock_get_queryset):
    url = reverse('transport', kwargs={'pk': mock_get_queryset.id})

    response = api_client.post(
        path=url,
        data=json.dumps({'company_id': 1}),
        content_type='application/json',
    )

    assert response.status_code == 200

    response = api_client.post(
        path=url,
        data=json.dumps({'company_id': 2}),
        content_type='application/json',
    )

    assert response.status_code == 400


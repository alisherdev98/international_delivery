from django.urls import path, include

from delivery.views import DeliveryTypeView, DeliveryView, TransportDeliveryView, DeliveryRetrieveView


url_patterns = [
    path('', include([
        path('', DeliveryView.as_view(), name='delivery'),
        path('<int:pk>/', include([
            path('', DeliveryRetrieveView.as_view(), name='delivery_retrieve'),
            path('transport/', TransportDeliveryView.as_view(), name='transport'),
        ])),  # TODO  take a look autoadd slash in ending url path
        path('type/', DeliveryTypeView.as_view(), name='delivery_type')
    ])),
]
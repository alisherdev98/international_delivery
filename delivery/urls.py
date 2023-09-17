from django.urls import path, include

from delivery.views import DeliveryTypeView, DeliveryView, DeliveryRetrieveView


url_patterns = [
    path('', include([
        path('', DeliveryView.as_view()),
        path('<int:pk>/', DeliveryRetrieveView.as_view()),  # TODO  take a look autoadd / in ending url path
        path('type/', DeliveryTypeView.as_view())
    ])),
]
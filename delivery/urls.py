from django.urls import path, include

from delivery.views import DeliveryTypeView, DeliveryView


url_patterns = [
    path('', include([
        path('', DeliveryView.as_view()),
        path('<int:pk>/', include([
            path('', DeliveryView.as_view()),
            path('transport/', ...),
        ])),  # TODO  take a look autoadd slash in ending url path
        path('type/', DeliveryTypeView.as_view())
    ])),
]
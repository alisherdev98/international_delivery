from django.contrib import admin
from django.urls import path, include

from delivery.urls import url_patterns as delivery_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include([
        path('delivery/', include(delivery_patterns)),
    ])),
]

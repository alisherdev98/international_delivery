from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls.static import static
from django.conf import settings

from delivery.urls import url_patterns as delivery_patterns

schema_view = get_schema_view(
    openapi.Info(
        title="International delivery API",
        #  version of the swagger doc
        default_version='v1',
        # first line that appears on the top of the doc
        description="International delivery description",
    ),
    public=True,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include([
        path('delivery/', include(delivery_patterns)),
    ])),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

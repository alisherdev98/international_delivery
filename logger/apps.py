from logging.config import dictConfig
from django.apps import AppConfig


class LoggerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'logger'

    def ready(self) -> None:
        dictConfig({
            'version': 1,
            'disable_existing_loggers': False,
            'handlers': {
                'outer_request': {
                    'level': 'INFO',
                    'class': 'logger.handlers.OuterRequestHandler',
                },
                'delivery_cost': {
                    'level': 'INFO',
                    'class': 'logger.handlers.DeliveryCostHandler',
                },
            },
            'loggers': {
                'outer_request': {
                    'level': 'INFO',
                    'handlers': ['outer_request'],
                },
                'delivery_cost': {
                    'level': 'INFO',
                    'handlers': ['delivery_cost'],
                },
            },
        })
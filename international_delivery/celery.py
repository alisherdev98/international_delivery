import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'international_delivery.settings')
app = Celery('international_delivery')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'processing_delivery_cost': {
        'task': 'process_delivery_ruble_cost',
        'schedule': crontab(minute='*/1'),
    },
}


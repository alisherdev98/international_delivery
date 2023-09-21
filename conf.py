import os
from django.conf import settings

DEBUG = int(os.environ.get('DEBUG', 0))

CBRDAILY_DOMAIN = os.environ.get('CBRDAILY_DOMAIN')
CBRDAILY_EXCHANGE_PATH = os.environ.get('CBRDAILY_EXCHANGE_PATH')

REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')

DB_ENGINE = os.environ.get('DB_ENGINE', "django.db.backends.sqlite3")
DB_NAME = os.environ.get('DB_NAME', settings.BASE_DIR / "db.sqlite3")
DB_USER = os.environ.get('DB_USER', 'user')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'password')
DB_HOST = os.environ.get('DB_HOST', 'locahost')
DB_PORT = os.environ.get('DB_PORT', '5432')

MONGO_HOST = os.environ.get('MONGO_HOST', 'localhost')
MONGO_PORT = os.environ.get('MONGO_PORT', '27017')

RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', 'localhost')
RABBITMQ_PORT = os.environ.get('RABBITMQ_PORT', '5672')
RABBITMQ_DEFAULT_USER = os.environ.get('RABBITMQ_DEFAULT_USER', 'admin')
RABBITMQ_DEFAULT_PASS = os.environ.get('RABBITMQ_DEFAULT_PASS', 'pass')

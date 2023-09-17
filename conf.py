import os

CBRDAILY_DOMAIN = os.environ.get('CBRDAILY_DOMAIN')
CBRDAILY_EXCHANGE_PATH = os.environ.get('CBRDAILY_EXCHANGE_PATH')

REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')
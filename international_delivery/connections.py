import abc
import pika
from pymongo import MongoClient

import conf


class AbstractConnection(abc.ABC):
    """
        Signlton for a single connection source
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AbstractConnection, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    @abc.abstractmethod
    def _initialize(self):
        ...

    # @abc.abstractmethod
    # def __enter__(self):
    #     ...

    # @abc.abstractmethod
    # def __exit__(self):
    #     ...


class RabbitMQConnection(AbstractConnection):
    def _initialize(self):
        credentials = pika.PlainCredentials(
            username=conf.RABBITMQ_DEFAULT_USER,
            password=conf.RABBITMQ_DEFAULT_PASS,
        )
        self._connection_params = pika.ConnectionParameters(
            host=conf.RABBITMQ_HOST,
            port=conf.RABBITMQ_PORT,
            credentials=credentials,
        )
        self._connection = pika.BlockingConnection(
            self._connection_params
        )
        self.queue_name = 'international_delivery'
        self._channel = self._connection.channel()
        self._queue = self._channel.queue_declare(queue=self.queue_name)

    def get_channel(self):
        return self._channel


class MongoDBConnection(AbstractConnection):
    def _initialize(self):
        self.client = MongoClient(f"mongodb://{conf.MONGO_HOST}:{conf.MONGO_PORT}/")
        self.db = self.client['international_delivery']

    def get_collection(self, collection_name):
        return self.db[collection_name]
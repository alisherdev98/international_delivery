from enum import Enum


class DeliveryTypeEnum(Enum):
    OTHERS = (1, 'Разное')
    CLOTHES = (2, 'Одежда')
    ELECTRONICS = (3, 'Электроника')

    def __init__(self, id, full_name) -> None:
        self.id = id
        self.full_name = full_name


class DeliveryCreatingTypeEnum(Enum):
    CELERY_WORKER = 0
    RABBITMQ_QUEUE = 1

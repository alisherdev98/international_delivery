from logging import Handler, LogRecord

from logger.models import OuterRequestModel
from logger.repositories import DeliveryLogRepository


class OuterRequestHandler(Handler):
    def emit(self, record):
        OuterRequestModel.objects.create(**record.log_extra_data)


class DeliveryCostHandler(Handler):
    def emit(self, record: LogRecord) -> None:
        DeliveryLogRepository().create(record.log_extra_data)

from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.sessions.models import Session

class DeliveryType(models.Model):
    name = models.CharField(verbose_name='имя', max_length=255)
    full_name = models.CharField(verbose_name='полное имя', max_length=255)


class Delivery(models.Model):
    name = models.CharField(verbose_name='название', max_length=255,)
    weight = models.PositiveSmallIntegerField(verbose_name='вес в киллограммах')
    type = models.ForeignKey(DeliveryType, on_delete=models.PROTECT, verbose_name='тип')
    content_cost = models.PositiveIntegerField(
        verbose_name='стоимость содержимого в долларах',
        validators=[MinValueValidator(1)],
    )
    delivery_cost = models.PositiveIntegerField(
        verbose_name='стоимость в рублях',
        validators=[MinValueValidator(1)],
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # TODO check updating field after Queryset.update or model.bulk_update
    session_key = models.ForeignKey(Session, on_delete=models.PROTECT, verbose_name='ключ сессии клиента')
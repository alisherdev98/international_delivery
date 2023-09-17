from django.db import models
from django.core.validators import MinValueValidator

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
    ruble_cost = models.PositiveIntegerField(
        verbose_name='стоимость в рублях',
        validators=[MinValueValidator(1)],
        null=True,
    )
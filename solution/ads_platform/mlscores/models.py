from django.db import models


class MlScore(models.Model):
    client = models.ForeignKey(
        "clients.Client",
        on_delete=models.CASCADE,
        verbose_name="Клиент"
    )
    advertiser = models.ForeignKey(
        "advertisers.Advertiser",
        on_delete=models.CASCADE,
        verbose_name="Рекламодатель",
    )
    score = models.IntegerField(verbose_name="Вес связи")

    class Meta:
        verbose_name = "Вес"
        verbose_name_plural = "Весы"

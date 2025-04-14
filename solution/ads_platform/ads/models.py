from django.db import models


class AdImpression(models.Model):
    client = models.ForeignKey(
        "clients.Client",
        on_delete=models.CASCADE,
        verbose_name="ID клиента"
    )
    campaign = models.ForeignKey(
        "campaigns.Campaign",
        on_delete=models.CASCADE,
        verbose_name="ID рекламы"
    )
    date = models.IntegerField(
        default=0,
        verbose_name="Дата показа"
    )
    price = models.IntegerField(
        default=0,
        verbose_name="Цена показа"
    )


class AdClick(models.Model):
    client = models.ForeignKey(
        "clients.Client",
        on_delete=models.CASCADE,
        verbose_name="ID клиента"
    )
    campaign = models.ForeignKey(
        "campaigns.Campaign",
        on_delete=models.CASCADE,
        verbose_name="ID рекламы"
    )
    date = models.IntegerField(
        default=0,
        verbose_name="Дата клика"
    )
    price = models.IntegerField(
        default=0,
        verbose_name="Цена клика"
    )

    class Meta:
        verbose_name = "Клик"
        verbose_name_plural = "Клики"

from django.conf import settings
from django.db import models


class Advertiser(models.Model):
    advertiser_id = models.UUIDField(primary_key=True, verbose_name="ID")
    name = models.CharField(max_length=255, verbose_name="Название")

    class Meta:
        verbose_name = "Рекламодатель"
        verbose_name_plural = "Рекламодатели"


class AdvertiserFile(models.Model):
    advertiser = models.ForeignKey("Advertiser", on_delete=models.CASCADE)
    file = models.FileField(storage=settings.S3)

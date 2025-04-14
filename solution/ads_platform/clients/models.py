from django.db import models


class ClientGender(models.TextChoices):
    male = "MALE"
    female = "FEMALE"


class Client(models.Model):
    client_id = models.UUIDField(primary_key=True, verbose_name="ID")
    login = models.CharField(verbose_name="Логин", max_length=256)
    age = models.IntegerField(verbose_name="Возраст")
    location = models.CharField(verbose_name="Локация", max_length=256)
    gender = models.CharField(
        choices=ClientGender,
        verbose_name="Пол",
        max_length=256
    )

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

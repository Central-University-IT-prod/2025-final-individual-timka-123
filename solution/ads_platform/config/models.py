from django.db import models


class Config(models.Model):
    key = models.CharField(max_length=50, unique=True)
    value = models.IntegerField()

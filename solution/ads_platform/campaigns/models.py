from django.db import models

from config.models import Config

from .schemas import TargetSchema


class CampaignTargetGender(models.TextChoices):
    male = "MALE"
    female = "FEMALE"
    all = "ALL"


class ModerationStatus(models.TextChoices):
    PROCESS = "process"
    FAIL = "fail"
    OK = "ok"


class Target(models.Model):
    gender = models.CharField(
        verbose_name="Пол", choices=CampaignTargetGender.choices,
        null=True
    )
    age_from = models.IntegerField(
        verbose_name="Минимальный возраст", null=True
    )
    age_to = models.IntegerField(
        verbose_name="Максимальный возраст", null=True
    )
    location = models.TextField(
        verbose_name="Локация", null=True
    )


class Campaign(models.Model):
    campaign_id = models.UUIDField(primary_key=True, verbose_name="ID")
    advertiser = models.ForeignKey(
        "advertisers.Advertiser",
        on_delete=models.CASCADE,
        verbose_name="ID рекламодателя"
    )
    impressions_limit = models.IntegerField(verbose_name="Лимит показов")
    clicks_limit = models.IntegerField(verbose_name="Лимит кликов")
    cost_per_impression = models.FloatField(
        verbose_name="Стоимость показа объявления"
    )
    cost_per_click = models.FloatField(
        verbose_name="Стоимость перехода по объявлению"
    )
    ad_title = models.CharField(
        max_length=255,
        verbose_name="Название"
    )
    ad_text = models.TextField(
        verbose_name="Текст объявления"
    )
    start_date = models.IntegerField(
        verbose_name="День старта показа объявления"
    )
    end_date = models.IntegerField(
        verbose_name="День окончания показа объявления"
    )

    # api-edited settings
    clicked_count = models.IntegerField(
        null=True,
        default=0,
        editable=False
    )
    impressions_count = models.IntegerField(
        null=True,
        default=0,
        editable=False
    )

    targeting = models.OneToOneField(
        Target, on_delete=models.CASCADE, verbose_name="Таргет рекламы",
    )

    # s3 file
    file_url = models.URLField(
        null=True, max_length=2048
    )

    @property
    def is_active(self) -> bool:
        current_date = Config.objects.get(key="current_time").value

        if self.clicked_count >= self.clicks_limit:
            return False

        if self.impressions_count > self.impressions_limit:
            return False

        if not (self.start_date <= current_date <= self.end_date):
            return False

        return True

    def dict(self):
        data = self.__dict__

        target = self.targeting
        data["targeting"] = TargetSchema(**target.__dict__)
        del data["targeting_id"]

        return data

    class Meta:
        verbose_name = "Кампания"
        verbose_name_plural = "Кампании"

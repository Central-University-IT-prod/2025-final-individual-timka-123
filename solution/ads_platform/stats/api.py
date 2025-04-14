from uuid import UUID

from django.shortcuts import get_object_or_404
from ninja import Router

from advertisers.models import Advertiser
from ads.models import AdClick, AdImpression
from campaigns.models import Campaign
from config.models import Config

from .schemas import StatSchema


router = Router()


@router.get("/campaigns/{campaign_id}", response=StatSchema)
def get_campaign_stat(
    request,
    campaign_id: UUID
):
    get_object_or_404(Campaign, campaign_id=campaign_id)
    stat = StatSchema(
        impressions_count=0,
        clicks_count=0,
        conversion=0,
        spent_impressions=0,
        spent_clicks=0,
        spent_total=0
    )

    clicks = AdClick.objects.filter(
        campaign_id=campaign_id
    )
    impressions = AdImpression.objects.filter(
        campaign_id=campaign_id
    )

    stat.clicks_count = len(clicks)
    stat.spent_clicks = sum([click.price for click in clicks])

    stat.impressions_count = len(impressions)
    stat.spent_impressions = sum(
        [impression.price for impression in impressions]
    )

    stat.spent_total = stat.spent_clicks + stat.spent_impressions

    try:
        stat.conversion = stat.clicks_count / stat.impressions_count * 100
    except ZeroDivisionError:
        stat.conversion = 0

    return stat


@router.get("/advertisers/{advertiser_id}/campaigns", response=StatSchema)
def get_advertiser_stat(
    request,
    advertiser_id: UUID
):
    get_object_or_404(Advertiser, advertiser_id=advertiser_id)
    stat = StatSchema(
        impressions_count=0,
        clicks_count=0,
        conversion=0,
        spent_clicks=0,
        spent_impressions=0,
        spent_total=0
    )

    campaigns = Campaign.objects.filter(
        advertiser_id=advertiser_id
    )
    for campaign in campaigns:
        clicks = AdClick.objects.filter(
            campaign_id=campaign.campaign_id
        )
        impressions = AdImpression.objects.filter(
            campaign_id=campaign.campaign_id
        )

        stat.clicks_count += len(clicks)
        stat.spent_clicks += sum([click.price for click in clicks])

        stat.impressions_count += len(impressions)
        stat.spent_impressions += sum(
            [impression.price for impression in impressions]
        )

        stat.spent_total += stat.spent_clicks + stat.spent_impressions

    try:
        stat.conversion = stat.clicks_count / stat.impressions_count * 100
    except ZeroDivisionError:
        stat.conversion = 0

    return stat


@router.get("/campaigns/{campaign_id}/daily", response=list[StatSchema])
def get_campaign_daily_stat(
    request,
    campaign_id: UUID
):
    current_date = Config.objects.get(key="current_time").value
    campaign = get_object_or_404(Campaign, campaign_id=campaign_id)

    data = []

    for date in range(current_date + 1):
        clicks = AdClick.objects.filter(
            campaign_id=campaign_id,
            date=date
        ).all()
        impressions = AdImpression.objects.filter(
            campaign_id=campaign_id,
            date=date
        )
        data.append(StatSchema(
            impressions_count=len(impressions),
            clicks_count=len(clicks),
            conversion=len(clicks) / len(impressions) * 100 if len(impressions) > 0 else 0,
            spent_impressions=len(impressions) * campaign.cost_per_impression,
            spent_clicks=len(clicks) * campaign.cost_per_click,
            spent_total=(len(impressions) * campaign.cost_per_impression +
                         len(clicks) * campaign.cost_per_click)
        ))

    return data


@router.get("/campaigns/advertisers/{advertiser_id}/daily",
            response=list[StatSchema])
def get_advertiser_daily_stat(
    request,
    advertiser_id: UUID
):
    current_date = Config.objects.get(key="current_time").value
    get_object_or_404(Advertiser, advertiser_id=advertiser_id)

    data = []

    for date in range(current_date + 1):
        clicks = AdClick.objects.filter(
            advertiser_id=advertiser_id,
            date=date
        ).all()
        impressions = AdImpression.objects.filter(
            advertiser_id=advertiser_id,
            date=date
        )
        data.append(StatSchema(
            impressions_count=len(impressions),
            clicks_count=len(clicks),
            conversion=(len(clicks) / len(impressions) * 100
                        if len(impressions) > 0 else 0),
            spent_impressions=sum(
                [impression.price for impression in impressions]
            ),
            spent_clicks=sum([click.price for click in clicks]),
            spent_total=(
                sum([impression.price for impression in impressions]) +
                sum([click.price for click in clicks]))
        ))

    return data

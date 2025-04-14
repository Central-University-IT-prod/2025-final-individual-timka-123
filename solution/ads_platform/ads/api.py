from uuid import UUID

from django.shortcuts import get_object_or_404
from django.db import models
from ninja import Router
from ninja.responses import Response
from ninja.errors import HttpError

from mlscores.models import MlScore
from campaigns.models import Campaign
from clients.models import Client
from config.models import Config

from .schemas import AdSchema, ClickRequestSchema
from .models import AdClick, AdImpression


router = Router()


@router.get("")
def get_ad_for_user(
    request,
    client_id: UUID
):
    client = get_object_or_404(Client, client_id=client_id)
    
    client_scores = MlScore.objects.filter(client_id=client_id).order_by('-score')
    
    if not client_scores:
        raise HttpError(status_code=404, message="We don't have good ads for you, sorry")

    all_potential_ads = []

    for score in client_scores:
        campaigns = Campaign.objects.filter(
            advertiser_id=score.advertiser_id,
        ).select_related('targeting').all()

        for campaign in campaigns:
            if not campaign.is_active:
                continue
            
            location_match = age_match = gender_match = True
            
            if campaign.targeting:
                location_match = campaign.targeting.location in ('ALL', client.location, None)
                gender_match = campaign.targeting.gender in ('ALL', client.gender, None)
                
                age_match = True
                if campaign.targeting.age_from and client.age < campaign.targeting.age_from:
                    age_match = False
                if campaign.targeting.age_to and client.age > campaign.targeting.age_to:
                    age_match = False

            if location_match and age_match and gender_match:
                try:
                    ctr = (campaign.clicked_count / max(campaign.impressions_count, 1))
                except:
                    ctr = 100
                relevance_score = ctr * score.score
                all_potential_ads.append((campaign, relevance_score))

    all_potential_ads.sort(key=lambda x: x[1], reverse=True)

    for campaign, _ in all_potential_ads:
        if not AdImpression.objects.filter(
            client_id=client.client_id,
            campaign_id=campaign.campaign_id
        ).exists():
            date = Config.objects.get(key="current_time").value
            AdImpression.objects.create(
                client_id=client.client_id,
                campaign_id=campaign.campaign_id,
                date=date,
                price=campaign.cost_per_impression
            )
            
            Campaign.objects.filter(campaign_id=campaign.campaign_id).update(
                impressions_count=models.F('impressions_count') + 1
            )

            return AdSchema(
                ad_id=campaign.campaign_id,
                ad_title=campaign.ad_title,
                ad_text=campaign.ad_text,
                advertiser_id=campaign.advertiser_id,
                file_url=campaign.file_url
            )

    raise HttpError(
        status_code=404,
        message="We haven't found suitable ads for you at the moment."
    )


@router.post("/{campaign_id}/click", response={
    204: None
})
def accept_click(
    request,
    campaign_id: str,
    click: ClickRequestSchema
):
    try:
        campaign = get_object_or_404(Campaign, campaign_id=campaign_id)
    except Exception as e:
        return Response(
            status=400,
            data={
                "detail": f"Error while processing click: {e}"
            }
        )

    try:
        AdClick.objects.get(
            client_id=click.client_id,
            campaign_id=campaign_id
        )
    except AdClick.DoesNotExist:
        date = Config.objects.get(key="current_time").value
        AdClick.objects.create(
            client_id=click.client_id,
            campaign_id=campaign_id,
            date=date,
            price=campaign.cost_per_click
        )

        campaign.clicked_count += 1
        campaign.save()
    except Exception as e:
        return Response(
            status=400,
            data={
                "detail": f"Error while processing click: {e}"
            }
        )

    return 204, None

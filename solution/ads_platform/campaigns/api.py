from uuid import UUID, uuid4

from django.conf import settings
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.errors import HttpError
from ninja.responses import Response

from config.models import Config
from utils import YaGpt
from ads_platform.schemas import ErrorSchema

from advertisers.models import AdvertiserFile

from .schemas import CampaignSchema, CreateCampaignSchema, \
    UpdateCampaignSchema
from .models import Campaign, Target


router = Router()


@router.post("/{advertiser_id}/campaigns", response={
    201: CampaignSchema,
    418: ErrorSchema,
    400: ErrorSchema
})
def create_campaign(
    request,
    advertiser_id: UUID,
    data: CreateCampaignSchema
) -> CampaignSchema:
    target = data.targeting
    if target.age_from and target.age_to and target.age_from > target.age_to:
        raise HttpError(
            status_code=400,
            message="From age must be lower than age_to"
        )
    
    if data.file_id:
        file = get_object_or_404(AdvertiserFile, id=data.file_id)
        if file.advertiser_id != advertiser_id:
            raise HttpError(status_code=403, message="You have not access to this file")
        url = settings.S3.url(file.file.name)
    else:
        url = None
    
    # moderation check
    try:
        moderation_enabled = Config.objects.get(key="moderation_enabled").value
    except Config.DoesNotExist:
        moderation_enabled = False
    if moderation_enabled:
        yagpt = YaGpt(
            folder_id=settings.YAGPT_FOLDER_ID,
            auth=settings.YAGPT_AUTH
        )
        # check text
        is_success = yagpt.check_text(data.ad_text)
        if not is_success:
            raise HttpError(status_code=418, message="Moderation is not passed (ad text)")
        
        # check title
        is_success = yagpt.check_text(data.ad_title)
        if not is_success:
            raise HttpError(status_code=418, message="Moderation is not passed (ad title)")
        
    # generate text
    if data.generate_text:
        yagpt = YaGpt(
            folder_id=settings.YAGPT_FOLDER_ID,
            auth=settings.YAGPT_AUTH
        )
        text = yagpt.generate_description(data.ad_title)
        data.ad_text = text

    campaign_data = data.dict(exclude={"targeting", "generate_text", "file_id"})
    target = Target.objects.create(**data.targeting.dict())
    campaign_data.update({
        "campaign_id": str(uuid4()),
        "advertiser_id": advertiser_id,
        "targeting_id": target.pk,
        "file_url": url
    })
    try:
        campaign = Campaign.objects.create(**campaign_data)
    except Exception as e:
        raise HttpError(
            status_code=400,
            message=f"Error creating campaign: {e}"
        )
    return Response(
        data=CampaignSchema(**campaign.dict()),
        status=201
    )


@router.get("/{advertiser_id}/campaigns/{campaign_id}")
def get_campaign(
    request,
    advertiser_id: UUID,
    campaign_id: UUID
) -> CampaignSchema:
    try:
        campaign = Campaign.objects.get(campaign_id=campaign_id)
    except Campaign.DoesNotExist:
        raise HttpError(status_code=404, message="Campaign not found")
    if advertiser_id != campaign.advertiser_id:
        raise HttpError(status_code=404, message="Campaign not found")

    return CampaignSchema(**campaign.dict())


@router.get("/{advertiser_id}/campaigns")
def get_advertiser_campaigns(
    request,
    advertiser_id: UUID,
    size: int = 10,
    page: int = 1
) -> list[CampaignSchema]:
    if size < 0 or page < 0:
        raise HttpError(status_code=400, message="Size or page params are incorrect")
    try:
        campaigns = Campaign.objects.filter(advertiser_id=advertiser_id).all()
    except Exception:
        raise HttpError(
            status_code=400,
            message="Something went wrong, maybe, advertiser's id is invalid"
        )
    page -= 1
    start_idx = page * size
    end_idx = start_idx + size
    filtered_campaigns = campaigns[start_idx:end_idx]
    schemed_campaigns = []
    for campaign in filtered_campaigns:
        schemed_campaigns.append(CampaignSchema(**campaign.dict()))
    return schemed_campaigns


@router.delete("/{advertiser_id}/campaigns/{campaign_id}")
def delete_campaign(
    request,
    advertiser_id: UUID,
    campaign_id: UUID
):
    try:
        campaign = Campaign.objects.get(campaign_id=campaign_id)
    except Campaign.DoesNotExist:
        raise HttpError(status_code=404, message="Campaign not found")
    if advertiser_id != campaign.advertiser_id:
        raise HttpError(status_code=404, message="Campaign not found")
    campaign.delete()
    return Response(
        status=204
    )


@router.put("/{advertiser_id}/campaigns/{campaign_id}")
def update_campaign(
    request,
    advertiser_id: UUID,
    campaign_id: UUID,
    data: UpdateCampaignSchema
) -> CampaignSchema:
    try:
        campaign = Campaign.objects.get(campaign_id=campaign_id)
    except Campaign.DoesNotExist:
        raise HttpError(status_code=404, message="Campaign not found")
    if advertiser_id != campaign.advertiser_id:
        raise HttpError(status_code=404, message="Campaign not found")
    
    current_date = Config.objects.get(key="current_date").value
    if not (campaign.start_date <= current_date <= campaign.end_date):
        raise HttpError(status_code=400, message="You cannot change any data after campaign started")
    
    if data.start_date > data.end_date:
        raise HttpError(status_code=400, message="Start date cannot be set before end date")
    
    if data.file_id:
        file = get_object_or_404(AdvertiserFile, id=data.file_id)
        if file.advertiser_id != advertiser_id:
            raise HttpError(status_code=403, message="You have not access to this file")
        url = settings.S3.url(file.file.name)
    else:
        url = None
    
    # moderation check
    try:
        moderation_enabled = Config.objects.get(key="moderation_enabled").value
    except Config.DoesNotExist:
        moderation_enabled = False
    if moderation_enabled:
        yagpt = YaGpt(
            folder_id=settings.YAGPT_FOLDER_ID,
            auth=settings.YAGPT_AUTH
        )
        # check text
        is_success = yagpt.check_text(data.ad_text)
        if not is_success:
            raise HttpError(status_code=418, message="Moderation is not passed (ad text)")
        
        # check title
        is_success = yagpt.check_text(data.ad_title)
        if not is_success:
            raise HttpError(status_code=418, message="Moderation is not passed (ad title)")

    campaign.cost_per_impression = data.cost_per_impression
    campaign.cost_per_click = data.cost_per_click
    campaign.ad_title = data.ad_title
    campaign.ad_text = data.ad_text
    campaign.start_date = data.start_date
    campaign.end_date = data.end_date
    campaign.impressions_limit = data.impressions_limit
    campaign.clicks_limit = data.clicks_limit
    campaign.targeting.location = data.targeting.location
    campaign.targeting.gender = data.targeting.gender
    campaign.targeting.age_from = data.targeting.age_from
    campaign.targeting.age_to = data.targeting.age_to

    if url:
        campaign.file_url = url

    campaign.save()
    campaign.targeting.save()

    return CampaignSchema(**campaign.dict())

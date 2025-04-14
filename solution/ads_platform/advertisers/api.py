from uuid import UUID

from ninja import Router, File
from ninja.files import UploadedFile
from ninja.errors import HttpError
from ninja.responses import Response

from .schemas import AdvertiserSchema, AdvertiserFileSchema
from .models import Advertiser, AdvertiserFile


router = Router()


@router.post(path="/bulk")
def bulk_ads_actions(
    request,
    advertisers: list[AdvertiserSchema]
) -> list[AdvertiserSchema]:
    advertiser_ids = [advertiser.advertiser_id for advertiser in advertisers]
    existing_advertisers = {adv.advertiser_id: adv for adv in Advertiser.objects.filter(advertiser_id__in=advertiser_ids)}

    new_advertisers = []
    for advertiser in advertisers:
        if advertiser.advertiser_id in existing_advertisers:
            db_advertiser = existing_advertisers[advertiser.advertiser_id]
            db_advertiser.name = advertiser.name
            db_advertiser.save()
        else:
            new_advertisers.append(Advertiser(**advertiser.dict()))

    if new_advertisers:
        Advertiser.objects.bulk_create(new_advertisers)

    return Response(
        data=advertisers,
        status=201
    )


@router.post(path="/{advertiser_id}/uploadfile")
def uploadfile(
    request,
    advertiser_id: UUID,
    file: UploadedFile = File(...)
):
    adv_file = AdvertiserFile.objects.create(
        advertiser_id=advertiser_id,
        file=file
    )
    return AdvertiserFileSchema(**adv_file.__dict__)


@router.get(path="/{advertiser_id}")
def get_advertiser(request, advertiser_id: UUID) -> AdvertiserSchema:
    try:
        advertiser = Advertiser.objects.get(
            advertiser_id=advertiser_id
        )
    except Advertiser.DoesNotExist:
        raise HttpError(status_code=404, message="Advertiser not found")

    return AdvertiserSchema(**advertiser.__dict__)

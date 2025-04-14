from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.responses import Response
from ninja.errors import HttpError

from clients.models import Client
from advertisers.models import Advertiser

from .schemas import MlScoreSchema
from .models import MlScore


router = Router()


@router.post("")
def set_ml_score(request, ml_score: MlScoreSchema):
    try:
        MlScore.objects.get(
            client_id=ml_score.client_id,
            advertiser_id=ml_score.advertiser_id
        )
    except MlScore.DoesNotExist:
        MlScore.objects.create(
            client_id=ml_score.client_id,
            advertiser_id=ml_score.advertiser_id,
            score=ml_score.score
        )
    except Exception as e:
        raise HttpError(status_code=400, message="Advertiser or client are not exists")

    return Response(
        data={"status": "ok"}
    )

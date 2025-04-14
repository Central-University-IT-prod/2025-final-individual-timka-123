from ninja import Router

from .schemas import TimeRequestSchema, ModerationStatusSchema
from config.models import Config

router = Router()


@router.get("/health")
def healthcheck(request):
    return "Test! tets! Test!"


@router.post("/time/advance", response={
    200: TimeRequestSchema
})
def set_internal_time(
    request,
    data: TimeRequestSchema
):
    try:
        config = Config.objects.get(key="current_time")
        config.value = data.current_date
        config.save()
    except Config.DoesNotExist:
        Config.objects.create(
            key="current_time",
            value=data.current_date
        )

    return data


@router.post("/moderation-status", response={
    200: ModerationStatusSchema
})
def set_moderation_status(
    request
):
    try:
        config = Config.objects.get(key="moderation_enabled")
        config.value = 1 if config.value == 0 else 0
        config.save()
    except Config.DoesNotExist:
        config = Config.objects.create(
            key="moderation_enabled",
            value=1
        )
    return ModerationStatusSchema(
        enabled=bool(config.value)
    )

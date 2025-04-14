from django.http import HttpResponse
from ninja import NinjaAPI
from ninja.errors import ValidationError


api = NinjaAPI(
    title="PROD 2025 final"
)
api.add_router(
    prefix="/clients",
    router="clients.api.router",
    tags=["clients"]
)
api.add_router(
    prefix="/advertisers",
    router="advertisers.api.router",
    tags=["advertisers"]
)
api.add_router(
    prefix="/ml-scores",
    router="mlscores.api.router",
    tags=["advertisers"]
)
api.add_router(
    prefix="/advertisers",
    router="campaigns.api.router",
    tags=["campaigns"]
)
api.add_router(
    prefix="/ads",
    router="ads.api.router",
    tags=["ads"]
)
api.add_router(
    prefix="/stats",
    router="stats.api.router",
    tags=["stats"]
)
api.add_router(
    prefix="",
    router="internal.api.router",
    tags=["internal"]
)


@api.exception_handler(ValidationError)
def validation_errors(request, exc):
    return HttpResponse(exc, status=400)

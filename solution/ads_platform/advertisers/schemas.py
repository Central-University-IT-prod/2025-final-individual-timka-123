from uuid import UUID

from ninja import Schema


class AdvertiserSchema(Schema):
    advertiser_id: UUID
    name: str


class AdvertiserFileSchema(Schema):
    id: int
    file: str

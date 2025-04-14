from uuid import UUID

from ninja import Schema


class MlScoreSchema(Schema):
    client_id: UUID
    advertiser_id: UUID
    score: int

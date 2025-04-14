from typing import Optional
from uuid import UUID
from ninja import Schema


class AdSchema(Schema):
    ad_id: UUID
    ad_title: str
    ad_text: str
    advertiser_id: UUID
    file_url: Optional[str] = None


class ClickRequestSchema(Schema):
    client_id: str

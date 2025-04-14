from typing import Optional, Literal
from uuid import UUID

from ninja import Schema


class TargetSchema(Schema):
    gender: Optional[Literal['MALE', 'FEMALE', 'ALL']] = None
    age_from: Optional[int] = None
    age_to: Optional[int] = None
    location: Optional[str] = None


class CreateCampaignSchema(Schema):
    impressions_limit: int
    clicks_limit: int
    cost_per_impression: float
    cost_per_click: float
    ad_title: str
    ad_text: str
    start_date: int
    end_date: int
    targeting: TargetSchema
    generate_text: Optional[bool] = False
    file_id: Optional[int] = None


class CampaignSchema(Schema):
    campaign_id: UUID
    advertiser_id: UUID
    impressions_limit: int
    clicks_limit: int
    cost_per_impression: float
    cost_per_click: float
    ad_title: str
    ad_text: str
    start_date: int
    end_date: int
    targeting: TargetSchema
    file_url: Optional[str] = None


class UpdateCampaignSchema(Schema):
    cost_per_impression: float
    impressions_limit: int
    clicks_limit: int
    cost_per_click: float
    ad_title: str
    ad_text: str
    start_date: int
    end_date: int
    targeting: TargetSchema
    file_id: Optional[str] = None

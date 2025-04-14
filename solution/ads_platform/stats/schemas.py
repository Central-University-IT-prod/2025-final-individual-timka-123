from ninja import Schema


class StatSchema(Schema):
    impressions_count: int
    clicks_count: int
    conversion: int
    spent_impressions: float
    spent_clicks: float
    spent_total: float

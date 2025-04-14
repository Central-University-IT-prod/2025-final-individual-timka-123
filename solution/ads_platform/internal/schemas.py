from ninja import Schema


class TimeRequestSchema(Schema):
    current_date: int


class ModerationStatusSchema(Schema):
    enabled: bool

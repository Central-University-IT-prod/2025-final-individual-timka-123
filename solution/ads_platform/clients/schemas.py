from uuid import UUID

from ninja import Schema


class ClientSchema(Schema):
    client_id: UUID
    login: str
    age: int
    location: str
    gender: str

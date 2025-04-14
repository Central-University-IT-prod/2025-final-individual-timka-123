from uuid import UUID
from ninja import Router
from ninja.errors import HttpError
from ninja.responses import Response

from .schemas import ClientSchema
from .models import Client


router = Router()


@router.post("/bulk")
def bulk_clients(request, clients: list[ClientSchema]):
    client_ids = [client.client_id for client in clients]
    existing_clients = {client.client_id: client for client in Client.objects.filter(client_id__in=client_ids)}

    new_clients = []
    for client in clients:
        if client.client_id in existing_clients:
            db_client = existing_clients[client.client_id]
            db_client.login = client.login
            db_client.location = client.location
            db_client.age = client.age
            db_client.gender = client.gender
            db_client.save()
        else:
            new_clients.append(Client(**client.dict()))

    if new_clients:
        Client.objects.bulk_create(new_clients)

    return Response(
        data=clients,
        status=201
    )


@router.get("/{client_id}")
def get_client(request, client_id: UUID) -> ClientSchema:
    try:
        client = Client.objects.get(client_id=client_id)
    except Client.DoesNotExist:
        raise HttpError(status_code=404, message="Client not found")
    return ClientSchema(**client.__dict__)

from typing import Any

from fastapi import APIRouter, Response, status

from fast_api_monolith_example.crud import (
    create_service,
    delete_service,
    get_service,
    get_services,
    update_service,
)
from fast_api_monolith_example.dependencies import CurrentUserDep, ServiceDep, SessionDep
from fast_api_monolith_example.models.services import Service, ServiceCreate, ServiceUpdate

router = APIRouter(prefix="/service", tags=["service"])


@router.get("/", response_model=list[Service])
def list_services(session: SessionDep, user: CurrentUserDep):
    get_services(session, user.id)


@router.get("/{service_id}", response_model=Service)
def get_service_by_id(session: SessionDep, user: CurrentUserDep, service: ServiceDep) -> Any:
    get_service(session, service)


@router.post("/", response_model=Service, status_code=status.HTTP_201_CREATED)
def service_create(session: SessionDep, payload: ServiceCreate, user: CurrentUserDep) -> Any:
    create_service(session, payload)


@router.patch("/{service_id}", response_model=Service)
def service_update(
    session: SessionDep, service: ServiceDep, payload: ServiceUpdate, user: CurrentUserDep
) -> Any:
    update_service(session, service, payload)


@router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
def service_delete(session: SessionDep, service: ServiceDep) -> Response:
    delete_service(session, service)

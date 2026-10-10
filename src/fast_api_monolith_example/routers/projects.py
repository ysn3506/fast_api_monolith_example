from typing import Any

from fastapi import APIRouter, Response
from starlette.status import HTTP_201_CREATED

from fast_api_monolith_example.crud import (
    create_project,
    delete_project,
    get_project,
    list_projects,
    update_project,
)
from fast_api_monolith_example.dependencies import CurrentUserDep, ProjectDep, SessionDep

from ..models.projects import Project, ProjectCreate, ProjectUpdate

router = APIRouter("/project", tags=["project"])


@router.get("/", response_model=list[Project])
def get_projects(session: SessionDep, user: CurrentUserDep) -> Any:
    list_projects(session, user.id)


@router.get("/{project_id}", response_model=Project)
def get_project_by_id(session: SessionDep, user: CurrentUserDep, project: ProjectDep) -> Any:
    get_project(session, project, user.id)


@router.post("/", response_model=Project, status_code=HTTP_201_CREATED)
def project_create(session: SessionDep, payload: ProjectCreate, user: CurrentUserDep) -> Any:
    create_project(session, payload)


@router.patch("/{project_id}", response_model=Project)
def project_update(
    session: SessionDep, user: CurrentUserDep, project: ProjectDep, payload: ProjectUpdate
) -> Any:
    update_project(session, project, payload)


@router.delete("/{project_id}")
def project_delete(session: SessionDep, user: CurrentUserDep, project: ProjectDep) -> Response:
    delete_project(session, project)

from typing import Annotated

from fastapi import Depends, HTTPException
from sqlmodel import Session

from .crud import get_project, get_service
from .db_config import get_db_session
from .models.auth import User
from .models.projects import Project
from .models.services import Service
from .security import get_current_user

SessionDep = Annotated[Session, Depends(get_db_session)]
CurrentUserDep = Annotated[User, Depends(get_current_user)]


def get_project_or_404(session: Session, project_id: int) -> Project | None:
    project = get_project(session, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project is not found")
    return project


ProjectDep = Annotated[Project, Depends(get_project_or_404)]


def get_service_or_404(session: Session, service_id: int) -> Service | None:
    service = get_service(session, service_id)
    if service is None:
        raise HTTPException(status_code=404, detail="Service is not found")
    return service


ServiceDep = Annotated[Service, Depends(get_service_or_404)]

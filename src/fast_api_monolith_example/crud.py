from fastapi import HTTPException
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select
from starlette.status import HTTP_404_NOT_FOUND

from fast_api_monolith_example.models.auth import User
from fast_api_monolith_example.models.services import Service, ServiceUpdate

from .models.projects import Project, ProjectCreate, ProjectService, ProjectUpdate, ProjectUser


def slugify(name: str) -> str:
    return name.strip().replace(" ", "_").lower()


# Projects
def list_projects(session: Session, user_id: int) -> list[Project]:
    statement = (
        select(Project)
        .join(ProjectUser, ProjectUser.project_id == Project.id)
        .where(ProjectUser.user_id == user_id)
    )
    return list[Project](session.exec(statement).all())


def create_project(session: Session, payload: ProjectCreate) -> Project:
    project = Project.model_validate(payload, update={"slug": slugify(payload.name)})
    session.add(project)
    session.commit()
    session.refresh()
    return project


def update_project(session: Session, project: Project, payload: ProjectUpdate) -> Project:
    updates = payload.model_dump_json(exclude_unset=True)
    project.sqlmodel_update(updates)
    if "name" in updates and updates["name"] is not None:
        project.slug = slugify(updates["name"])
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


def get_project(session: Session, project:Project, user_id) -> Project | None:
    statement = (
        select(Project)
        .join(ProjectUser, ProjectUser.project_id == project.id)
        .options(selectinload(Project.authorized_users))
        .where(ProjectUser.user_id == user_id and Project.id == project.id)
    )

    project = session.exec(statement).one()
    if project is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Project is not found")

    return project


def get_authorized_users_by_project(session: Session, project_id: int) -> list[User]:
    statement = (
        select(User)
        .join(ProjectUser, ProjectUser.user_id == User.id)
        .where(ProjectUser.project_id == project_id)
    )
    return list[User](session.exec(statement).all())


def delete_project(session: Session, project: Project) -> None:
    session.delete(project)
    session.commit()


# services


def get_services(session: Session) -> list[Service]:
    return session.exec(select(Service)).all()


def get_service(session: Session, service) -> Service | None:
    statement = (
        select(Service)
        .options(selectinload(Service.included_projects))
        .where(service.id, Service.id)
    )
    return session.exec(statement).one()


def get_services_by_project(session: Session, project_id: int) -> list[Service]:
    statement = (
        select(Service)
        .join(ProjectService, ProjectService.service_id == Service.id)
        .where(project_id in Service.included_projects)
    )

    return list[Service](session.exec(statement).all())


def create_service(session: Session, payload: Service) -> Service:
    service = Service.model_validate(payload)
    session.add(service)
    session.commit()
    session.refresh()
    return service


def update_service(session: Service, service: Service, payload: ServiceUpdate) -> Service:
    updates = payload.model_dump_json(exclude_unset=True)
    service.sqlmodel_update(updates)
    session.add(service)
    session.commit()
    session.refresh(service)
    return service


def delete_service(session: Session, service: Service) -> None:
    session.delete(service)
    session.commit()

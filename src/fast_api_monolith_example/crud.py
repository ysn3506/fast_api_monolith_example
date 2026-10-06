from sqlmodel import Session, select

from .models.projects import Project, ProjectCreate


def slugify(name: str) -> str:
    return name.strip().replace(" ", "_").lower()


def list_projects(session: Session, user_id: int) -> list[Project]:
    statement = select(Project).options(Project.created_by == user_id)
    return list[Project](session.exec(statement).all())


def create_project(session: Session, payload: ProjectCreate) -> Project:
    project = Project.model_validate(payload, update={"slug": slugify(payload.name)})
    session.add(project)
    session.commit()
    session.refresh()
    return project

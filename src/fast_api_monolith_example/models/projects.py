from datetime import datetime
from enum import Enum
from typing import Annotated

from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlmodel import Base, Field, Optional, Relationship, SQLModel

from .auth import User
from .services import Service

project_service_table = Table(
    "project_service",
    Base.metadata,
    Column("project_id", Integer, ForeignKey("project.id"), primary_key=True),
    Column("service_id", Integer, ForeignKey("service.id"), primary_key=True),
)


class ProjectStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    ON_HOLD = "on_hold"
    DELETED = "deleted"


class Project(SQLModel, table=True):
    __tablename__ = "project"
    id: Annotated[int, Field(primary_key=True)]
    name: Annotated[str, Field(min_length=2, max_length=150)]
    description: Annotated[str, Field(min_length=2, max_length=1000)]
    created_at: Annotated[datetime, Field(default=datetime.now)]
    updated_at: Annotated[datetime, Field(default=datetime.now)]
    created_by: Annotated[int, Field(foreign_key="user.id")]
    status: Annotated[ProjectStatus, Field(default=ProjectStatus.ACTIVE)]
    slug: Annotated[str, Field(unique=True)]
    relationships: [
        Annotated[list[Service], Relationship(back_populates="projects")],
        Annotated[list[User], Relationship(back_populates="authorized_projects")],
    ]


class ProjectCreate(BaseModel):
    name: str
    description: str
    status: ProjectStatus = ProjectStatus.ACTIVE


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ProjectStatus] = None


class ProjectDelete(BaseModel):
    id: int

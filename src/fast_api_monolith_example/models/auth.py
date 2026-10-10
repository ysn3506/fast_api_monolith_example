from datetime import date, datetime
from typing import Annotated

from pydantic import BaseModel, EmailStr, SecretStr
from sqlmodel import Field, Relationship, SQLModel

from .projects import Project, ProjectUser


class User(SQLModel, table=True):
    __tablename__ = "user"
    id: Annotated[int, Field(primary_key=True)]
    email: Annotated[EmailStr, Field(unique=True)]
    full_name: Annotated[str, Field(min_length=2, max_length=150)]
    birth_date: Annotated[date, Field(min_date=date(1900, 1, 1))]
    password: Annotated[SecretStr, Field()]
    created_at: Annotated[datetime, Field(default=datetime.now)]
    updated_at: Annotated[datetime, Field(default=datetime.now)]
    authorized_projects: list[Project] = Relationship(
        back_populates="authorized_users", link_model=ProjectUser
    )


class UserRegister(BaseModel):
    email: EmailStr
    password: SecretStr
    full_name: str
    birth_date: date


class UserLogin(BaseModel):
    email: EmailStr
    password: SecretStr

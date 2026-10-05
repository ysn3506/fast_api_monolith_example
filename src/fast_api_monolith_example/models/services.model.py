from datetime import datetime
from typing import Annotated

from pydantic import BaseModel
from sqlmodel import Field, Optional, SQLModel


class Service(SQLModel, table=True):
    __tablename__ = "service"
    id: Annotated[int, Field(primary_key=True)]
    name: Annotated[str, Field(min_length=2, max_length=150)]
    description: Annotated[str, Field(min_length=2, max_length=1000)]
    created_at: Annotated[datetime, Field(default=datetime.now)]
    updated_at: Annotated[datetime, Field(default=datetime.now)]


class ServiceCreate(BaseModel):
    name: str
    description: str
    
class ServiceUpdate(BaseModel):
    id: int
    name: Optional[str] = None
    description: Optional[str] = None

class ServiceDelete(BaseModel):
    id: int
import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PostCreate(BaseModel):
    author_agent_id: uuid.UUID
    title: str = Field(min_length=2, max_length=255)
    content: str = Field(min_length=10, max_length=10000)


class PostResponse(BaseModel):
    id: uuid.UUID
    author_agent_id: uuid.UUID
    author_name: str
    title: str
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

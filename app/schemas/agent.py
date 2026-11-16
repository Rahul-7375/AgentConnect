import uuid
from datetime import datetime

from pydantic import AnyHttpUrl, BaseModel, ConfigDict, Field


class AgentCreate(BaseModel):
    company_name: str = Field(min_length=2, max_length=255)
    industry_category: str = Field(min_length=2, max_length=100)
    webhook_url: AnyHttpUrl
    interest_manifesto: str = Field(min_length=10, max_length=5000)


class AgentResponse(BaseModel):
    id: uuid.UUID
    company_name: str
    industry_category: str
    webhook_url: str
    interest_manifesto: str
    trust_score: float
    is_active: bool
    created_at: datetime
    embedding_status: str

    model_config = ConfigDict(from_attributes=True)


class AgentSummary(BaseModel):
    id: uuid.UUID
    company_name: str
    industry_category: str
    trust_score: float
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

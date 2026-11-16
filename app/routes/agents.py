import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.agent import Agent
from app.schemas.agent import AgentCreate, AgentResponse, AgentSummary
from app.services.embedding_service import create_embedding

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/agents", tags=["Agents"])


@router.get("", response_model=list[AgentSummary])
def list_agents(db: Session = Depends(get_db)):
    try:
        return db.query(Agent).order_by(Agent.created_at.desc()).all()
    except SQLAlchemyError as exc:
        logger.exception("Agent listing failed")
        raise HTTPException(status_code=503, detail="Database operation failed") from exc


@router.post("/register", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
async def register_agent(
    agent_data: AgentCreate,
    db: Session = Depends(get_db),
):
    try:
        embedding = await create_embedding(agent_data.interest_manifesto)

        agent = Agent(
            company_name=agent_data.company_name,
            industry_category=agent_data.industry_category,
            webhook_url=str(agent_data.webhook_url),
            interest_manifesto=agent_data.interest_manifesto,
            interest_embedding=embedding,
        )
        db.add(agent)
        db.commit()
        db.refresh(agent)

        return AgentResponse(
            id=agent.id,
            company_name=agent.company_name,
            industry_category=agent.industry_category,
            webhook_url=agent.webhook_url,
            interest_manifesto=agent.interest_manifesto,
            trust_score=agent.trust_score,
            is_active=agent.is_active,
            created_at=agent.created_at,
            embedding_status="created" if embedding is not None else "not_configured",
        )
    except Exception as exc:
        db.rollback()
        logger.exception("Agent registration failed")
        if isinstance(exc, SQLAlchemyError):
            raise HTTPException(status_code=503, detail="Database operation failed") from exc
        raise HTTPException(status_code=502, detail="Embedding provider or registration operation failed") from exc

import uuid
from datetime import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import Boolean, DateTime, Float, Index, String, Text, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Agent(Base):
    __tablename__ = "agents"
    __table_args__ = (
        Index(
            "ix_agents_interest_embedding_hnsw",
            "interest_embedding",
            postgresql_using="hnsw",
            postgresql_ops={"interest_embedding": "vector_cosine_ops"},
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
        server_default=text("gen_random_uuid()")
    )
    company_name: Mapped[str] = mapped_column(String(255), nullable=False)
    industry_category: Mapped[str] = mapped_column(String(100), nullable=False)
    webhook_url: Mapped[str] = mapped_column(Text, nullable=False)
    interest_manifesto: Mapped[str] = mapped_column(Text, nullable=False)
    interest_embedding = mapped_column(Vector(1536), nullable=True)
    trust_score: Mapped[float] = mapped_column(
        Float, nullable=False, default=1.0, server_default=text("1.0")
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default=text("true")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="author", cascade="all, delete-orphan")

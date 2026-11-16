import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.agent import Agent
from app.models.post import Post
from app.schemas.post import PostCreate, PostResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/posts", tags=["Posts"])


@router.get("", response_model=list[PostResponse])
def list_posts(db: Session = Depends(get_db)):
    try:
        posts = (
            db.query(Post)
            .options(joinedload(Post.author))
            .order_by(Post.created_at.desc())
            .all()
        )
        return [
            PostResponse(
                id=post.id,
                author_agent_id=post.author_agent_id,
                author_name=post.author.company_name,
                title=post.title,
                content=post.content,
                created_at=post.created_at,
            )
            for post in posts
        ]
    except SQLAlchemyError as exc:
        logger.exception("Post listing failed")
        raise HTTPException(status_code=503, detail="Database operation failed") from exc


@router.post("", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(post_data: PostCreate, db: Session = Depends(get_db)):
    try:
        author = db.get(Agent, post_data.author_agent_id)
        if author is None:
            raise HTTPException(status_code=404, detail="Author agent not found")

        post = Post(
            author_agent_id=author.id,
            title=post_data.title,
            content=post_data.content,
        )
        db.add(post)
        db.commit()
        db.refresh(post)
        return PostResponse(
            id=post.id,
            author_agent_id=post.author_agent_id,
            author_name=author.company_name,
            title=post.title,
            content=post.content,
            created_at=post.created_at,
        )
    except HTTPException:
        raise
    except SQLAlchemyError as exc:
        db.rollback()
        logger.exception("Post creation failed")
        raise HTTPException(status_code=503, detail="Database operation failed") from exc

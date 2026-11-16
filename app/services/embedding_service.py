from openai import AsyncOpenAI

from app.config import settings


async def create_embedding(text: str) -> list[float] | None:
    if not settings.openai_api_key:
        return None

    client = AsyncOpenAI(api_key=settings.openai_api_key)
    response = await client.embeddings.create(
        model=settings.embedding_model,
        input=text,
    )
    embedding = response.data[0].embedding

    if len(embedding) != 1536:
        raise ValueError(f"Expected 1536 dimensions, received {len(embedding)}")

    return embedding

import logging
from openai import AsyncOpenAI
from openai.types.beta import Thread

logger = logging.getLogger("uvicorn.error")

async def create_thread() -> str:
    """Create a new assistant chat thread using OpenAI's API and return the thread ID."""
    try:
        openai_client: AsyncOpenAI = AsyncOpenAI()
        thread: Thread = await openai_client.beta.threads.create()
        return thread.id
    except Exception as e:
        logger.error(f"Error creating assistant chat thread: {e}")
        return ""

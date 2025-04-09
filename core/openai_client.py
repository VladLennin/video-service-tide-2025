from fastapi import HTTPException

from openai import AsyncAzureOpenAI

from core.config import settings
from core.logger_config import get_logger

logger = get_logger(__name__)

client = AsyncAzureOpenAI(
    api_key=settings.dalle_api_key,
    azure_endpoint=settings.azure_endpoint,
    api_version="2024-02-15-preview"
)


async def generate_image(prompt: str) -> str:
    logger.info(f"Started gen image with prompt : {prompt}")
    try:
        response = await client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        logger.info(f"Image generated: {response.data[0].url}")
        return response.data[0].url
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
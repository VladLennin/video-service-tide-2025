from openai import AsyncAzureOpenAI

from core.config import settings

client = AsyncAzureOpenAI(
    api_key=settings.dalle_api_key,
    azure_endpoint=settings.azure_endpoint,
    api_version="2024-02-15-preview"
)


async def generate_image(prompt: str) -> str:
    response = await client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    return response.data[0].url

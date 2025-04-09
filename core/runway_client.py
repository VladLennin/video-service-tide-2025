from typing import Literal

from fastapi import HTTPException
from runwayml import AsyncRunwayML
import asyncio

from core.config import settings
from core.logger_config import get_logger

client = AsyncRunwayML(
    api_key=settings.runwayml_api_key,
)

logger = get_logger(__name__)


async def start_generating_video(prompt_text: str, prompt_image_url: str, duration: Literal[5, 10] = 5) -> str:
    logger.info(
        f"Started generating video\n prompt: {prompt_text}, prompt_image_url: {prompt_image_url}, duration: {duration}")
    try:
        video = await client.image_to_video.create(
            model="gen3a_turbo",
            prompt_image=prompt_image_url,
            prompt_text=prompt_text,
            duration=duration
        )
        logger.info(
            f"Task for generating video ID: {video.id}")
        return video.id
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=429, detail="You have reached daily generations limit")


async def get_video_url(task_id: str, timeout: int = 300, interval: int = 5):
    for _ in range(0, timeout, interval):
        task_status = await client.tasks.retrieve(task_id)

        if task_status.status == "SUCCEEDED":
            logger.info(
                f"Video with id:{task_id} was generated, url: {task_status.output}")
            return task_status.output

        elif task_status.status == "FAILED":
            raise Exception("Video generation failed")

        await asyncio.sleep(interval)

    raise TimeoutError("Video generation timed out")

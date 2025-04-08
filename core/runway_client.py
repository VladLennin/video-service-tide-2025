from typing import Literal

from runwayml import AsyncRunwayML
import asyncio

from core.config import settings

client = AsyncRunwayML(
    api_key=settings.runwayml_api_key,
)


async def start_generating_video(prompt_text: str, prompt_image_url: str, duration: Literal[5, 10] = 5) -> str:
    video = await client.image_to_video.create(
        model="gen3a_turbo",
        prompt_image=prompt_image_url,
        prompt_text=prompt_text,
        duration=duration
    )
    return video.id


async def get_video_url(task_id: str, timeout: int = 300, interval: int = 5):
    for _ in range(0, timeout, interval):
        task_status = await client.tasks.retrieve(task_id)

        if task_status.status == "SUCCEEDED":
            return task_status.output

        elif task_status.status == "FAILED":
            raise Exception("Video generation failed")

        await asyncio.sleep(interval)

    raise TimeoutError("Video generation timed out")

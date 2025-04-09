from typing import Literal, Optional

from pydantic import BaseModel


class VideoFromImage(BaseModel):
    prompt: str
    image_url: str
    duration: Literal[5, 10] = 5


class VideoCollectionRequest(BaseModel):
    start_image_url: Optional[str] = None
    start_image_prompt: Optional[str] = None
    prompts: list[str]


class VideoFromText(BaseModel):
    image_prompt: str
    video_prompt: str
    duration: Literal[5, 10] = 5

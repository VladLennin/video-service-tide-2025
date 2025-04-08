from typing import Literal

from pydantic import BaseModel


class VideoFromImage(BaseModel):
    prompt: str
    image_url: str
    duration: Literal[5, 10] = 5


class VideoCollectionRequest(BaseModel):
    starting_image_url: str
    prompts: list[str]


class VideoFromText(BaseModel):
    image_prompt: str
    video_prompt: str
    duration: Literal[5, 10] = 5

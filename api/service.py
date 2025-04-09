import base64
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Literal
from urllib.parse import urlparse
from moviepy import VideoFileClip, concatenate_videoclips

import aiohttp
import aiofiles
from fastapi import HTTPException

def generate_unique_filename(file_url: str) -> str:
    parsed_url = urlparse(file_url)
    original_name = os.path.basename(parsed_url.path)
    _, ext = os.path.splitext(original_name)

    unique_name = f"{uuid.uuid4().hex}{ext}"
    return unique_name

async def download_file(url: str, media_type: Literal["video", "image"], ):
    directory = "images" if media_type == "image" else "videos"
    save_path = os.path.join(directory, generate_unique_filename(file_url=url))

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                raise HTTPException(status_code=resp.status, detail=f"Failed to download file from {url}")
            f = await aiofiles.open(save_path, mode='wb')
            await f.write(await resp.read())
            await f.close()
        return save_path


async def extract_last_frame(video_path: str) -> str:
    output_image_dir = Path("images")
    output_image_dir.mkdir(parents=True, exist_ok=True)

    output_image_path = output_image_dir / f"{uuid.uuid4().hex}.png"

    with VideoFileClip(video_path) as video:
        video.save_frame(str(output_image_path), t=video.duration - 0.05)

    return str(output_image_path)

def get_image_base64(image_path:str ):
    with open(image_path, "rb") as f:
        base64_image = base64.b64encode(f.read()).decode("utf-8")
    prompt_image = f"data:image/png;base64,{base64_image}"
    return prompt_image


async def concatenate_videos(video_paths: list[str]) -> str:
    clips = [VideoFileClip(path) for path in video_paths]

    final_clip = concatenate_videoclips(clips, method="compose")

    output_dir = Path("videos")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_filename = output_dir / f"{datetime.now()}_{uuid.uuid4().hex}_final.mp4"
    final_clip.write_videofile(str(output_filename), codec="libx264")

    for clip in clips:
        clip.close()
    final_clip.close()

    return str(output_filename)
from fastapi import APIRouter, HTTPException

from api.schemas import VideoFromImage, VideoFromText, VideoCollectionRequest
from core.config import settings
from core.logger_config import get_logger
from core.openai_client import generate_image
from core.runway_client import get_video_url, start_generating_video
from api.service import download_file, extract_last_frame, get_image_base64, concatenate_videos

router = APIRouter(
    prefix=settings.api_prefix
)

logger = get_logger("generate-prompts")


@router.post("/gen-video-from-image")
async def gen_videos(video_from_image: VideoFromImage):
    logger.info(
        f"Started generating video from image:{video_from_image.image_url}, prompt:{video_from_image.prompt}, duration:{video_from_image.duration}")
    video_id = await start_generating_video(
        prompt_text=video_from_image.prompt,
        prompt_image_url=video_from_image.image_url
    )
    logger.info(f"Created task for video, ID: {video_id}")
    video_url = await get_video_url(task_id=video_id)
    logger.info(f"Generated video URL: {video_url}")
    await download_file(url=video_from_image.image_url, media_type="image")
    await download_file(url=video_url[0], media_type="video")

    return video_url


@router.get("/get-video/{id}")
async def get_video_by_id(video_id: str):
    return await get_video_url(task_id=video_id)


@router.post("/gen-image")
async def gen_image(prompt: str):
    logger.info(f"Started gen image with prompt : {prompt}")
    image_url = await generate_image(prompt=prompt)
    logger.info(f"Generated video URL : {image_url}")
    await download_file(url=image_url, media_type="image")

    return image_url


@router.post("/gen-video-from-text")
async def get_video_from_text(video_from_text: VideoFromText):
    try:
        logger.info(
            f"Started generating image from text, image_prompt: {video_from_text.image_prompt},  video_prompt:{video_from_text.video_prompt}, duration: {video_from_text.duration}"
        )
        image_url = await generate_image(prompt=video_from_text.image_prompt)
        await download_file(url=image_url, media_type="image")

        logger.info(f"Generated video with URL:{image_url}")
        video_id = await start_generating_video(
            prompt_text=video_from_text.video_prompt,
            prompt_image_url=image_url
        )
        logger.info(f"Created task for generating video, URL:{video_id}")

        video_url = await get_video_url(task_id=video_id)

        await download_file(url=video_url[0], media_type="video")

        logger.info(f"Video generated, URL:{video_url}")
        return {"image_source": image_url, "video_url": video_url}
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/gen-video-collection")
async def gen_video_collection(video_collection: VideoCollectionRequest):
    result = []
    previous_image_url = video_collection.starting_image_url

    for prompt_text in video_collection.prompts:
        video_queue_id = await start_generating_video(
            prompt_text=prompt_text,
            prompt_image_url=previous_image_url
        )

        video_urls = await get_video_url(task_id=video_queue_id)
        video_url = video_urls[0]

        local_path = await download_file(url=video_url, media_type="video")

        result.append(video_url)

        previous_image_path = await extract_last_frame(local_path)

        previous_image_url = get_image_base64(image_path=previous_image_path)

    concatenated_video = await concatenate_videos(result)
    return {"generated_videos": result, "concatenated_video": concatenated_video}

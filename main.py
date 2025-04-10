import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.router import router as api_router
from core.config import settings
from pathlib import Path

main_app = FastAPI(
)

main_app.include_router(api_router)

Path("images").mkdir(parents=True, exist_ok=True)
main_app.mount("/videos", StaticFiles(directory="videos"), name="videos")

Path("videos").mkdir(parents=True, exist_ok=True)

main_app.mount("/images", StaticFiles(directory="images"), name="images")
main_app.mount("/videos", StaticFiles(directory="videos"), name="videos")

if __name__ == "__main__":
    uvicorn.run("main:main_app", host=settings.host, port=settings.port, reload=True)
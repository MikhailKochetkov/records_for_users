import os

from fastapi import FastAPI, APIRouter

from api.handlers import router
from settings import (
    UPLOADED_FILES,
    WAV_UPLOADED_FILES,
    MP3_UPLOADED_FILES)


if not os.path.exists(UPLOADED_FILES):
    os.mkdir(UPLOADED_FILES)
if not os.path.exists(MP3_UPLOADED_FILES):
    os.mkdir(MP3_UPLOADED_FILES)
if not os.path.exists(WAV_UPLOADED_FILES):
    os.mkdir(WAV_UPLOADED_FILES)

app = FastAPI(title='Create users and save audio records')
main_router = APIRouter()

main_router.include_router(router)
app.include_router(main_router)

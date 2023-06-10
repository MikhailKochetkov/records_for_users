import os
from dotenv import load_dotenv

load_dotenv()


DEV_MODE = True
HOST = os.getenv("HOST", default="127.0.0.1")
PORT = os.getenv("PORT", default=8000)
UPLOADED_FILES = "./media/"
MP3_UPLOADED_FILES = UPLOADED_FILES + "mp3/"
WAV_UPLOADED_FILES = UPLOADED_FILES + "wav/"

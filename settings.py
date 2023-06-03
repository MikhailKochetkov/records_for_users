import os
from dotenv import load_dotenv

load_dotenv()


HOST = os.getenv('HOST', default='127.0.0.1')
PORT = os.getenv('PORT', default=8000)
UPLOADED_FILES = "./media/"

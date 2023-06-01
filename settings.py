import os
from dotenv import load_dotenv

load_dotenv()


DATABASE_URL = f"sqlite:///./{os.getenv('DB_NAME', default='database.db')}"
# DATABASE_URL = "postgresql://postgres:postgresql@localhost/db"
HOST = os.getenv('HOST', default='127.0.0.1')
PORT = os.getenv('PORT', default=8000)
UPLOADED_FILES = "./media/"

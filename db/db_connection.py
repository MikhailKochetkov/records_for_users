import os
from dotenv import load_dotenv

load_dotenv()


CONNECTION_STRING = (f'{os.getenv("PG_DB_URL", default="postgresql+asyncpg://")}'
                     f'{os.getenv("POSTGRES_USER", default="postgres")}:'
                     f'{os.getenv("POSTGRES_PASSWORD", default="postgres")}'
                     f'@'
                     f'{os.getenv("DB_HOST", default="db")}:'
                     f'{os.getenv("DB_PORT", default=5432)}/'
                     f'{os.getenv("POSTGRES_DB", default="records")}')

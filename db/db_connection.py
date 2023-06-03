import os
from dotenv import load_dotenv

load_dotenv()


CONNECTION_STRING = (f'{os.getenv("DATABASE_URL", default="sqlite:///")}'
                     f'./{os.getenv("DB_NAME", default="database.db")}')

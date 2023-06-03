from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .db_connection import CONNECTION_STRING


engine = create_engine(CONNECTION_STRING, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

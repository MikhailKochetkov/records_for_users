from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .db_connection import CONNECTION_STRING, PG_CONNECTION_STRING
from settings import DEV_MODE
from .models import User, Record


if DEV_MODE:
    engine = create_engine(CONNECTION_STRING, connect_args={"check_same_thread": False})
    User.metadata.create_all(engine)
    Record.metadata.create_all(engine)
    SessionLocal = sessionmaker(autoflush=False, bind=engine)
else:
    engine = create_engine(PG_CONNECTION_STRING)
    User.metadata.create_all(engine)
    Record.metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

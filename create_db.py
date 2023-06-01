from sqlalchemy import create_engine

from settings import DATABASE_URL
from db.models import User, Record


def main():
    engine = create_engine(DATABASE_URL)
    User.metadata.create_all(engine)
    Record.metadata.create_all(engine)


if __name__ == '__main__':
    main()

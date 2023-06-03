from sqlalchemy import create_engine

from db.db_connection import CONNECTION_STRING
from db.models import User, Record


def main():
    engine = create_engine(CONNECTION_STRING)
    User.metadata.create_all(engine)
    Record.metadata.create_all(engine)


if __name__ == '__main__':
    main()

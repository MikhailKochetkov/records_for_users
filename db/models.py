from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )
    name = Column(String)
    email: Mapped[str] = mapped_column(String, unique=True)
    token: Mapped[str] = mapped_column(String, unique=True)
    records = relationship('Record', back_populates='owner')


class Record(Base):
    __tablename__ = 'records'

    id: Mapped[int] = mapped_column(
        UUID(as_uuid=True), primary_key=True, index=True
    )
    file_name: Mapped[str] = mapped_column(String)
    orig_file_name: Mapped[str] = mapped_column(String)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    owner = relationship('User', back_populates='records')

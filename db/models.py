from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    token = Column(String, unique=True)
    records = relationship('Record', back_populates='owner')


class Record(Base):
    __tablename__ = 'records'

    id = Column(String, primary_key=True, index=True)
    file_name = Column(String)
    orig_file_name = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship('User', back_populates='records')

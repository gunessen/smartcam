import datetime

from sqlalchemy import Column, DateTime, Integer, String

from .base import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    video_path = Column(String, nullable=False)
    objects = Column(String, nullable=True)
    event_time = Column(DateTime, nullable=False)
    video_length = Column(Integer, nullable=False)
    created_at = Column(String, nullable=False, default=datetime.datetime.now(datetime.UTC))


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False)
    created_at = Column(String, nullable=False, default=datetime.datetime.now(datetime.UTC))


class Settings(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    setting_name = Column(String, nullable=False)
    setting_value = Column(String, nullable=False)

import datetime

from sqlalchemy import Column, Integer, String

from .base import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    video_path = Column(String, nullable=False)
    objects = Column(String, nullable=True)
    created_at = Column(String, nullable=False, default=datetime.datetime.now(datetime.UTC))

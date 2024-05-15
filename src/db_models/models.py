import datetime

from sqlalchemy import Column, Integer, String

from .base import Base


# Define a Video class to store video information in the database
class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(String, nullable=False)
    objects = Column(String, nullable=True)
    created_at = Column(String, nullable=False, default=datetime.datetime.now(datetime.UTC))

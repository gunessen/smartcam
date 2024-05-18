from datetime import datetime

from db_models.base import Session
from db_models.models import Event


def add_event(video_path: str, objects: dict, event_time: datetime, video_length: int):
    """
    Add an event to the database.

    :param video_path: the path to the video
    :param objects: the objects detected in the video
    """
    session = Session()
    event = Event(
        video_path=video_path,
        objects=str(objects),
        event_time=event_time,
        video_length=video_length,
    )
    session.add(event)
    session.commit()
    session.close()


def get_events():
    """
    Get all events from the database.

    :return: a list of events
    """
    session = Session()
    events = session.query(Event).all()
    session.close()
    return events


def get_event(event_id: int):
    """
    Get a specific event from the database.

    :param event_id: the id of the event to get
    :return: the event
    """
    session = Session()
    event = session.query(Event).filter(Event.id == event_id).first()
    session.close()
    return event

from db_models.base import Session
from db_models.models import Event


def add_event(video_path, objects):
    """
    Add an event to the database.

    :param video_path: the path to the video
    :param objects: the objects detected in the video
    """
    session = Session()
    event = Event(
        video_path=video_path,
        objects=objects,
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

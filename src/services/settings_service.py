from db_models.base import Session
from db_models.models import Settings

# def add_event(video_path: str, objects: dict, event_time: datetime, video_length: int):
#     """
#     Add an event to the database.

#     :param video_path: the path to the video
#     :param objects: the objects detected in the video
#     """
#     session = Session()
#     event = Event(
#         video_path=video_path,
#         objects=str(objects),
#         event_time=event_time,
#         video_length=video_length,
#     )
#     session.add(event)
#     session.commit()
#     session.close()


def get_settings():
    """
    Get all events from the database.

    :return: a list of events
    """
    session = Session()
    settings = session.query(Settings).all()
    session.close()
    return settings

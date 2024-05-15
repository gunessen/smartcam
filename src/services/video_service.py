from db_models.base import Session
from db_models.models import Video


def add_video(path, objects):
    """
    Add a video to the database.

    :param path: the path to the video
    :param objects: the objects detected in the video
    """
    session = Session()
    video = Video(
        path=path,
        objects=objects,
    )
    session.add(video)
    session.commit()
    session.close()

from flask import Blueprint, jsonify, make_response, send_file

from backend.schemas import EventSchema
from services import event_service

events_bp = Blueprint("events", __name__)


@events_bp.route("/api/v1/events", methods=["GET"])
def get_events():
    """
    Get all events from the database.

    :return: a list of events
    """
    events = event_service.get_events()
    return jsonify(EventSchema(many=True).dump(events))


@events_bp.route("/api/v1/events/<int:event_id>", methods=["GET"])
def get_event(event_id):
    """
    Get a specific event from the database.

    :param event_id: the id of the event to get
    :return: the event
    """
    event = event_service.get_event(event_id)
    return jsonify(EventSchema().dump(event))


@events_bp.route("/api/v1/events/<int:event_id>/video", methods=["GET"])
def get_video(event_id):
    """
    Get the video of a specific event from the database.

    :param event_id: the id of the event to get the video for
    :return: the video
    """
    event = event_service.get_event(event_id)

    import os

    print(event.video_path)
    print(os.path.exists(event.video_path))
    filename = os.path.basename(event.video_path)
    print(filename)
    response = make_response(send_file(event.video_path, mimetype="video/mp4"))
    response.headers["Content-Disposition"] = (
        f"inline; filename={os.path.basename(event.video_path)}"
    )
    return response

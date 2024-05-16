from flask import Blueprint, jsonify

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

from flask import Blueprint, jsonify, request

from backend.schemas import SettingsSchema
from services import settings_service

settings_bp = Blueprint("settings", __name__)


@settings_bp.route("/api/v1/settings", methods=["GET"])
def get_settings():
    """
    Get all settings from the database.

    :return: a dict of settings
    """
    settings_dict = settings_service.get_settings()

    return jsonify(SettingsSchema().dump(settings_dict))


@settings_bp.route("/api/v1/settings", methods=["PUT"])
def update_settings():
    """
    Update the settings in the database.

    :return: None
    """
    for s in request.json:
        settings_service.update_setting(s, request.json[s])

    return jsonify({"message": "Settings updated successfully."})

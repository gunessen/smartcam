from flask import Blueprint, jsonify

from backend.schemas import SettingsSchema
from services import settings_service

settings_bp = Blueprint("settings", __name__)


@settings_bp.route("/api/v1/settings", methods=["GET"])
def get_settings():
    """
    Get all settings from the database.

    :return: a list of settings
    """
    settings = settings_service.get_settings()

    # Map the settings to a dictionary
    settings_dict = {setting.setting_name: setting.setting_value for setting in settings}

    return jsonify(SettingsSchema().dump(settings_dict))
